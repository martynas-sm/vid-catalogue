from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
        examples=["adomas"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address",
        examples=["adomas@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password",
        examples=["secretpassword123"],
    )


class UserLoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Account username",
        examples=["adomas"],
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Account password",
        examples=["secretpassword123"],
    )
    totp_code: str | None = Field(
        default=None,
        min_length=6,
        max_length=6,
        description="Optional 6-digit TOTP code if 2FA is enabled",
        examples=["123456"],
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="Signed JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    refresh_token: str = Field(
        ...,
        description="Opaque refresh token string",
        examples=["a1b2c3d4e5f6g7h8..."],
    )
    token_type: str = Field(
        default="bearer",
        description="OAuth2 token type",
        examples=["bearer"],
    )


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        min_length=1,
        description="Opaque refresh token string",
        examples=["a1b2c3d4e5f6g7h8..."],
    )


class TokenRefreshResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="New signed JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="OAuth2 token type",
        examples=["bearer"],
    )


class TOTPSetupResponse(BaseModel):
    secret: str = Field(
        ...,
        description="Base32 TOTP secret key for manual entry",
        examples=["JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"],
    )
    otpauth_uri: str = Field(
        ...,
        description="otpauth:// provisioning URI for QR code generation",
        examples=[
            "otpauth://totp/VideoCatalogue:adomas?secret=JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP&issuer=VideoCatalogue"
        ],
    )


class TOTPVerifyRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="6-digit TOTP verification code",
        examples=["123456"],
    )
