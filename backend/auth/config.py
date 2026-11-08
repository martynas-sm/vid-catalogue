import os

# JWT Signing Secret Key (can be overridden via JWT_SECRET_KEY or SECRET_KEY env var)
# To generate a new production key: openssl rand -hex 32
SECRET_KEY: str = os.getenv(
    "JWT_SECRET_KEY",
    os.getenv(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    ),
)

# JWT Signing Algorithm (HS256 recommended for symmetric key signatures)
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

# Access token lifespan in minutes (short-lived)
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Refresh token lifespan in days (long-lived)
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
