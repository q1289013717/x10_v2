from pydantic_settings import BaseSettings
from pydantic import computed_field
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "X10增长引擎 API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "X10增长引擎后端服务 - Vue3 + Python + PostgreSQL"

    SECRET_KEY: str = "x10-engine-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    DATABASE_URL: str = "sqlite:///./x10.db"

    # CORS — 因为 pydantic-settings 对 list 字段会先 json.loads，所以用 str 存储
    # 支持格式： "*" 、 '["http://a.com","http://b.com"]'（JSON数组）、逗号分隔
    CORS_ORIGINS_RAW: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176"

    @property
    def cors_origins(self) -> list[str]:
        """解析 CORS_ORIGINS_RAW 为 list"""
        s = self.CORS_ORIGINS_RAW.strip()
        if s == "*":
            return ["*"]
        # 尝试 JSON 数组
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        # 逗号分隔
        return [x.strip() for x in s.split(",") if x.strip()]

    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_URL.startswith("postgresql")

    @property
    def is_mysql(self) -> bool:
        return self.DATABASE_URL.startswith("mysql")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
