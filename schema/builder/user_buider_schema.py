import uuid
from typing import Optional

from pydantic import ValidationError
from schema.base.user_base_schema import UserBaseSchema


class UserBuilderSchema:
    def __init__(self):
        self._data = {}

    def set_role_id(self, role_id: uuid.UUID):
        self._data[UserBaseSchema.ROLE_ID] = role_id
        return self

    def set_org_id(self, org_id: uuid.UUID):
        self._data[UserBaseSchema.ORG_ID] = org_id
        return self

    def set_display_name(self, display_name: str):
        self._data[UserBaseSchema.DISPLAY_NAME] = display_name
        return self

    def set_password_hash(self, password_hash: str):
        self._data[UserBaseSchema.PASSWORD_HASH] = password_hash
        return self

    def set_email(self, email: str):
        self._data[UserBaseSchema.EMAIL] = email
        return self

    def set_phone_number(self, phone_number: Optional[str]):
        self._data[UserBaseSchema.PHONE_NUMBER] = phone_number
        return self

    def set_avatar_url(self, avatar_url: Optional[str]):
        self._data[UserBaseSchema.AVATAR_URL] = avatar_url
        return self

    def set_avatar_fallback(self, avatar_fallback: Optional[str]):
        self._data[UserBaseSchema.AVATAR_FALLBACK] = avatar_fallback
        return self

    def set_is_verified(self, is_verified: bool):
        self._data[UserBaseSchema.IS_VERIFIED] = is_verified
        return self

    def set_is_change_password(self, is_change_password: bool):
        self._data[UserBaseSchema.IS_CHANGE_PASSWORD] = is_change_password
        return self

    def set_verification_code(self, verification_code: Optional[str]):
        self._data[UserBaseSchema.VERIFICATION_CODE] = verification_code
        return self

    def build(self):
        try:
            return UserBaseSchema(**self._data)
        except ValidationError as e:
            print("❌ Validation Error:", e)
            return None