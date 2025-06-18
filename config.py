import os


class Config:
    # Base config shared by all environments
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Cache settings
    CACHE_TYPE = os.environ.get("CACHE_TYPE") or "RedisCache"
    CACHE_REDIS_URL = (
        os.environ.get("CACHE_REDIS_URL") or "redis://localhost:6379/1"
    )  # Use DB 1 for cache (db 0 is typically used by Celery)
    CACHE_DEFAULT_TIMEOUT = int(
        os.environ.get("CACHE_DEFAULT_TIMEOUT") or 300
    )  # 5 minutes default


class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = os.environ.get("CACHE_TYPE") or "SimpleCache"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or Config.SQLALCHEMY_DATABASE_URI
    )


class ProductionConfig(Config):
    if (
        not Config.SECRET_KEY
        or Config.SECRET_KEY == "a-default-hardcoded-secret-key-change-me"
    ):
        raise ValueError(
            "SECRET_KEY must be set via environment variable in production"
        )
    pass


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or Config.SQLALCHEMY_DATABASE_URI
    )

    CACHE_TYPE = "NullCache"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
