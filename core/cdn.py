import os
import uuid
from typing import Dict, Optional

import boto3
import filetype
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from loguru import logger

from core.env import env

# Constants
KB = 1024
MB = 1024 * KB
MAX_FILE_SIZE = 150 * MB

# File type configurations
SUPPORTED_FILE_TYPES = {
    # Images
    "image/png": "images/png",
    "image/jpeg": "images/jpeg",
    
    # Documents
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docs",
    "text/plain": "text",
    "application/msword": "docs",
    
    # Excel files
    "application/vnd.ms-excel": "excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "excel",
    "application/xlsx": "excel",
    
    # Videos
    "video/mp4": "videos",
    "video/quicktime": "videos",
    "video/x-msvideo": "videos",
    "video/webm": "videos",
    "video/x-ms-wmv": "videos"
}

# Excel file signatures for manual detection
EXCEL_SIGNATURES = {
    b'PK\x03\x04': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX
    b'\xD0\xCF\x11\xE0': "application/vnd.ms-excel",  # XLS
}

class CDNHandler:
    def __init__(self):
        self.session = boto3.Session()
        self.cdn_resource = self.session.resource("s3")
        self.bucket = self.cdn_resource.Bucket(env.AWS_BUCKET)

    async def validate_file_size(self, file: UploadFile) -> None:
        """Validate file size is within limits"""
        contents = await file.read()
        size = len(contents)
        await file.seek(0)
        if not 0 < size <= MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File size must be between 0 and {MAX_FILE_SIZE/MB:.0f}MB"
            )

    def get_file_type(self, contents: bytes, filename: str) -> str:
        """Determine file type using multiple methods"""
        # Try magic number detection first
        kind = filetype.guess(contents)
        if kind and kind.mime in SUPPORTED_FILE_TYPES:
            return kind.mime

        # Check Excel signatures
        for signature, mime_type in EXCEL_SIGNATURES.items():
            if contents.startswith(signature):
                return mime_type

        # Check file extension as fallback
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.xlsx', '.xls']:
            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported types are {list(SUPPORTED_FILE_TYPES.keys())}"
        )

    def generate_file_location(self, filename: str, file_type: str) -> str:
        """Generate unique CDN file path"""
        folder = SUPPORTED_FILE_TYPES.get(file_type, "files")
        file_extension = os.path.splitext(filename)[1].lower()
        return f"{folder}/{uuid.uuid4()}{file_extension}"

    async def upload_file(self, contents: bytes, key: str, content_type: Optional[str] = None) -> None:
        """Upload file to CDN"""
        try:
            extra_args = {"ContentType": content_type} if content_type else {}
            self.bucket.put_object(Key=key, Body=contents, **extra_args)
            
            # Verify upload
            obj = self.cdn_resource.Object(bucket_name=env.AWS_BUCKET, key=key)
            if obj.content_length == 0:
                raise HTTPException(status_code=500, detail="Failed to upload file")
                
        except ClientError as err:
            logger.error(f"CDN upload error: {str(err)}")
            raise HTTPException(status_code=500, detail="Failed to upload file")

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate URL for file access (CloudFront or CDN presigned URL)"""
        try:
            # Use CloudFront if enabled
            if env.USE_CLOUDFRONT and env.CLOUDFRONT_DOMAIN:
                return self._get_cloudfront_url(key)
            
            # Fall back to CDN presigned URL if CloudFront is not enabled
            cdn_client = self.session.client("s3")
            return cdn_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": env.AWS_BUCKET, "Key": key},
                ExpiresIn=expires_in
            )
        except Exception as err:
            logger.error(f"URL generation error: {str(err)}")
            raise HTTPException(status_code=500, detail="Failed to generate file URL")

    async def delete_file(self, key: str) -> bool:
        """Delete file from CDN"""
        try:
            self.cdn_resource.Object(bucket_name=env.AWS_BUCKET, key=key).delete()
            return True
        except ClientError as err:
            logger.error(f"CDN delete error: {str(err)}")
            return False

    async def download_file(self, key: str) -> Optional[bytes]:
        """Download file from CDN"""
        try:
            obj = self.cdn_resource.Object(bucket_name=env.AWS_BUCKET, key=key)
            return obj.get()["Body"].read()
        except ClientError as err:
            logger.error(f"CDN download error: {str(err)}")
            return None

    async def list_files(self) -> Optional[list]:
        """List all files in bucket"""
        try:
            return [obj.key for obj in self.bucket.objects.all()]
        except ClientError as err:
            logger.error(f"CDN list error: {str(err)}")
            return None

    async def cdn_delete_file(self, key: str) -> bool:
        """Alias for delete_file for backward compatibility"""
        return await self.delete_file(key)

    def _get_cloudfront_url(self, key: str) -> str:
        """Generate a CloudFront URL with the correct format"""
        # Remove trailing slash from domain if present
        domain = env.CLOUDFRONT_DOMAIN.rstrip('/')
        # Ensure key doesn't start with a slash
        clean_key = key.lstrip('/')
        return f"{domain}/{clean_key}"

# Initialize CDN handler
cdn_handler = CDNHandler()