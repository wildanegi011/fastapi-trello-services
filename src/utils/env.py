"""Centralized environment configuration.

This module loads environment variables once and provides typed access
to prevent multiple load_dotenv() calls across the codebase.

Key Benefits:
- Single load_dotenv() call (instead of 6+ scattered calls)
- Typed access with proper defaults
- Clear separation between production and development variables
- Built-in validation helpers for deployment readiness
- Strict validation using get_env_var pattern for required variables
"""

import os

from dotenv import load_dotenv

load_dotenv()

class EnvConfig:
    """Centralized environment configuration."""

    def get_env_var(self, name: str, default: str | None = None) -> str:
        """Get an environment variable or return a default value.

        This method provides strict validation - raises ValueError if required
        environment variables are missing.

        Args:
            name: The name of the environment variable
            default: Optional default value if the environment variable is not set

        Returns:
            The value of the environment variable

        Raises:
            ValueError: If the environment variable is not set and no default is provided

        """
        value = os.environ.get(name)
        if value is None:
            if default is None:
                raise ValueError(f"Environment variable {name} is not set and no default provided")
            else:
                print(f"Environment variable {name} is not set, using default value: {default}")
                return default
        return value

    # =====================================================================
    # Project Configuration
    # =====================================================================
    @property
    def project_name(self) -> str:
        """Get the project name."""
        return self.get_env_var("PROJECT_NAME")

    @property
    def version(self) -> str:
        """Get the project version."""
        return self.get_env_var("VERSION")

    # =====================================================================
    # Database Configuration
    # =====================================================================

    @property
    def database_url(self) -> str:
        """Get the database URL."""
        return self.get_env_var("DATABASE_URL")


env = EnvConfig()
