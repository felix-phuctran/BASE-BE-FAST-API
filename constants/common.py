class AppTranslationKeys:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppTranslationKeys, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Authentication related messages
        self.Auth = {
            "InvalidCredentials": "errors.auth.invalid_credentials",
            "SessionExpired": "errors.auth.session_expired",
            "SessionCreationFailed": "errors.auth.session_creation_failed",
            "UnauthorizedAccess": "errors.auth.unauthorized_access",
            "TokenGenerationFailed": "errors.auth.token_generation_failed",
            "PasswordResetEmailSent": "messages.auth.password_reset_email_sent",
            "PasswordResetFailed": "errors.auth.password_reset_failed",
            "InvalidResetToken": "errors.auth.invalid_reset_token",
            "PasswordResetSuccess": "messages.auth.password_reset_success",
            "InvalidPassword": "errors.auth.invalid_password",
            "PasswordChangeFailed": "errors.auth.password_change_failed",
            "PasswordChangeSuccess": "messages.auth.password_change_success",
            "NotEnoughPermissions": "errors.auth.not_enough_permissions",
            "TokenExpired": "errors.auth.token_expired",
            "InvalidTokenType": "errors.auth.invalid_token_type",
            "UserNotFound": "errors.auth.user_not_found",
            "InactiveUser": "errors.auth.inactive_user",
            "UnverifiedUser": "errors.auth.unverified_user",
            "AdminRequired": "errors.auth.admin_required",
        }

        # SignIn related messages
        self.SignIn = {
            "Failed": "errors.sign_in.failed",
            "WithDraw": "errors.sign_in.withdraw",
            "InvalidAttempt": "errors.sign_in.invalid_attempt",
            "AccountLocked": "errors.sign_in.account_locked",
        }

        # Token related messages
        self.Token = {
            "Invalid": "errors.token.invalid",
            "Generated": "errors.token.generated",
            "Required": "errors.token.required",
            "NotVerified": "errors.token.not_verified",
            "AlreadyUse": "errors.token.already_use",
            "Expired": "errors.token.expired",
            "RefreshFailed": "errors.token.refresh_failed",
        }

        # User related messages
        self.User = {
            "RequiredFields": "errors.user.required_fields",
            "CannotDelete": "errors.user.cannot_delete",
            "NotFound": "errors.user.notfound",
            "Invalid": "errors.user.invalid",
            "PasswordInvalid": "errors.user.password_invalid",
            "PasswordRequired": "errors.user.password_required",
            "UpdatedFailed": "errors.user.updated_failed",
            "CreatedFailed": "errors.user.created_failed",
            "EmailExist": "errors.user.email_exist",
            "CannotRegister": "errors.user.cannot_register",
            "InviteCodeNotExist": "errors.user.invite_code_not_exist",
            "AlreadyGotInviteCode": "errors.user.already_got_invite_code",
            "NicknameExist": "errors.user.nickname_exist",
            "UserInvalid": "errors.user.user_invalid",
            "UpdateFireBaseTokenFailed": "errors.user.update_firebase_token_failed",
            "ProfileIsSelected": "errors.user.profile_is_selected",
            "ProfileNotEmpty": "errors.user.profile_not_empty",
            "EmailOrPasswordInvalid": "errors.user.email_or_password_invalid",
            "AccountDisabled": "errors.user.account_disabled",
            "InsufficientPermissions": "errors.user.insufficient_permissions",
            "UserAlreadyExists": "errors.user.user_already_exists",
            "UserCreationFailed": "errors.user.user_creation_failed",
            "UserNotVerified": "errors.user.user_not_verified",
            "VerificationEmailFailed": "errors.user.verification_email_failed",
            "VerificationSuccess": "messages.user.verification_success",
            "VerificationFailed": "errors.user.verification_failed",
            "InvalidVerificationCode": "errors.user.invalid_verification_code",
            "RoleAssignSuccess": "messages.user.role_assign_success",
            "RoleAssignFailed": "errors.user.role_assign_failed",
            "AccountLockSuccess": "messages.user.account_lock_success",
            "AccountLockFailed": "errors.user.account_lock_failed",
            "AccountUnlockSuccess": "messages.user.account_unlock_success",
            "AccountUnlockFailed": "errors.user.account_unlock_failed",
        }

        # Session related messages
        self.Session = {
            "CreationFailed": "errors.session.creation_failed",
            "InvalidSession": "errors.session.invalid",
            "Expired": "errors.session.expired",
            "NotFound": "errors.session.not_found",
            "AlreadyExists": "errors.session.already_exists",
        }

        # Third party authentication providers
        self.ThirdPartyAuth = {
            "Google": "Google",
            "Apple": "Apple",
            "Phone": "Phone",
            "Email": "Email",
            "Facebook": "Facebook",
            "AuthFailed": "errors.third_party.auth_failed",
        }

        # Authentication types
        self.AuthType = {"Refresh": "refresh", "Access": "access", "TwoFactor": "2fa"}

        # Add Role translations
        self.Role = {"RoleNotFound": "errors.role.not_found"}

    def get_message(self, category: str, key: str) -> str:
        """Helper method to safely get translation messages"""
        category_dict = getattr(self, category, {})
        return category_dict.get(key, f"Missing translation: {category}.{key}")
