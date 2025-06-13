"""Tests for configuration management."""

import os
from pathlib import Path

import pytest

from e3_e4.config import Settings, get_settings, get_test_settings


class TestSettings:
    """Test settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = get_test_settings()
        
        assert settings.app_name == "CollibrIA"
        assert settings.environment == "development"
        assert settings.debug is True
        assert settings.log_level == "INFO"
        assert settings.aws_region == "eu-west-3"

    def test_environment_override(self, monkeypatch):
        """Test environment variable override."""
        # Set environment variables
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("DEBUG", "false")
        monkeypatch.setenv("LOG_LEVEL", "ERROR")
        
        settings = Settings()
        
        assert settings.environment == "production"
        assert settings.debug is False
        assert settings.log_level == "ERROR"

    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid log level
        settings = get_test_settings(log_level="debug")
        assert settings.log_level == "DEBUG"
        
        # Invalid log level should raise error
        with pytest.raises(ValueError, match="Invalid log level"):
            get_test_settings(log_level="INVALID")

    def test_database_url_property(self):
        """Test database URL construction."""
        settings = get_test_settings(
            database_user="testuser",
            database_password="testpass",
            database_host="localhost",
            database_port=3306,
            database_name="testdb",
        )
        
        expected_url = "mysql://testuser:testpass@localhost:3306/testdb"
        assert settings.database_url == expected_url

    def test_is_production_property(self):
        """Test is_production property."""
        dev_settings = get_test_settings(environment="development")
        assert dev_settings.is_production is False
        assert dev_settings.is_development is True
        
        prod_settings = get_test_settings(environment="production")
        assert prod_settings.is_production is True
        assert prod_settings.is_development is False

    def test_settings_from_env_file(self, tmp_path, monkeypatch):
        """Test loading settings from .env file."""
        # Create temporary .env file
        env_file = tmp_path / ".env"
        env_file.write_text(
            """
APP_NAME=TestApp
ENVIRONMENT=staging
LOG_LEVEL=DEBUG
AWS_REGION=us-east-1
"""
        )
        
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        settings = Settings()
        
        assert settings.app_name == "TestApp"
        assert settings.environment == "staging"
        assert settings.log_level == "DEBUG"
        assert settings.aws_region == "us-east-1"

    def test_get_settings_singleton(self):
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2