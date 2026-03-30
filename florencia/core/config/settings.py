"""Global configuration using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class GlobalConfig(BaseConfig):
    """Global application configuration."""

    env: str = Field(default="DEV", description="Environment: DEV, PRO, PRE, UNITTEST")
    debug: bool = Field(default=True, description="Debug mode")
    database_type: str = Field(default="sqlite", description="Database type: sqlite, postgres")
    database_uri: str = Field(default="", description="Full database connection URI")
    log_level: str = Field(default="DEBUG", description="Logging level")
    path_data: Path = Field(default=Path("data"), description="Data directory path")
    path_logs: Path = Field(default=Path("data/log"), description="Logs directory path")

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.env == "DEV"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "PRO"

    @property
    def is_testing(self) -> bool:
        """Check if running in test mode."""
        return self.env == "UNITTEST"


class DevConfig(GlobalConfig):
    """Development configuration."""

    debug: bool = True
    log_level: str = "DEBUG"


class ProConfig(GlobalConfig):
    """Production configuration."""

    debug: bool = False
    log_level: str = "INFO"


class PreConfig(GlobalConfig):
    """Pre-production configuration."""

    debug: bool = False
    log_level: str = "INFO"


class UnitTestConfig(GlobalConfig):
    """Unit test configuration."""

    debug: bool = True
    env: str = "UNITTEST"
    log_level: str = "TRACE"
    database_type: str = "sqlite"
    database_uri: str = ":memory:"


CONFIG_MAP = {
    "DEV": DevConfig,
    "PRO": ProConfig,
    "PRE": PreConfig,
    "UNITTEST": UnitTestConfig,
}


@lru_cache
def get_config() -> GlobalConfig:
    """Get configuration based on environment variable."""
    env = GlobalConfig().env
    config_class = CONFIG_MAP.get(env, DevConfig)
    return config_class()


class DriConfig:
    """YAML configuration loader."""

    def __init__(self) -> None:
        self._config: dict[str, object] | None = None

    def load(self, config_file: str = "florencia/config/config.yaml") -> dict[str, object]:
        """Load YAML configuration file."""
        if self._config is None:
            config_path = Path(config_file)
            if config_path.exists():
                import yaml

                with open(config_path) as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = {}
        return self._config

    @property
    def app_config(self) -> dict[str, object]:
        """Get application configuration."""
        return self.load()


config = DriConfig()
