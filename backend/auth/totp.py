import pyotp


def generate_totp_secret() -> str:
    """Generate a random 32-character Base32 secret for TOTP (RFC 6238)."""
    return pyotp.random_base32()


def get_provisioning_uri(
    username: str,
    secret: str,
    issuer_name: str = "VideoCatalogue",
) -> str:
    """Generate an otpauth:// provisioning URI for authenticator app enrollment."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)


def verify_totp_code(secret: str, code: str, valid_window: int = 1) -> bool:
    """Verify a 6-digit TOTP code against the Base32 secret.

    Allows +/-valid_window counter intervals (+/-30s drift per interval).
    Returns True if valid, False otherwise.
    """
    if not secret or not code:
        return False

    clean_code = str(code).strip()
    try:
        totp = pyotp.TOTP(secret)
        return bool(totp.verify(clean_code, valid_window=valid_window))
    except Exception:
        return False
