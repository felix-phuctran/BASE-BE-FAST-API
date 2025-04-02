import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict

import httpx
from fastapi import HTTPException
from utils.logger import setup_logger

logger = setup_logger()



async def get(
    url: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None
) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            full_url = httpx.URL(url).copy_with(params=params)
            logger.info(f"Making GET request to: {full_url}")
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error for URL {e.request.url}: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request Error for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def post(
    url: str, data: Dict[str, Any] = None, headers: Dict[str, Any] = None
) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            full_url = httpx.URL(url)
            logger.info(f"Making POST request to: {full_url}")
            logger.info(f"Data: {data}")
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error for URL {e.request.url}: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request Error for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def put(
    url: str, data: Dict[str, Any] = None, headers: Dict[str, Any] = None
) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            full_url = httpx.URL(url)
            logger.info(f"Making PUT request to: {full_url}")
            response = await client.put(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error for URL {e.request.url}: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request Error for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def delete(url: str, headers: Dict[str, Any] = None) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            full_url = httpx.URL(url)
            logger.info(f"Making DELETE request to: {full_url}")
            response = await client.delete(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error for URL {e.request.url}: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request Error for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


import asyncio

if __name__ == "__main__":
    response = asyncio.run(get(url="http://127.0.0.1:8001/api/v1/health", headers=None, params=None))
    print(response)