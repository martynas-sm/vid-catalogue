import pyotp


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_provisioning_uri(
    username: str,
    secret: str,
    issuer_name: str = "VideoCatalogue",
) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)


def verify_totp_code(secret: str, code: str, valid_window: int = 1) -> bool:
    if not secret or not code:
        return False
    try:
        return bool(pyotp.TOTP(secret).verify(str(code).strip(), valid_window=valid_window))
    except Exception:
        return False
