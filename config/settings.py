"""Application settings and configuration."""

from typing import Dict, Any
import os

class Settings:
    """Application settings configuration."""
    
    def __init__(self):
        self.app_title = "BID OPTIMIZER"
        self.version = "1.0.0"
        self.environment = os.getenv("ENV", "development")
        
        # UI Settings
        self.dark_mode = True
        self.show_debug_info = self.environment == "development"
        
        # Session settings
        self.session_timeout = 3600  # 1 hour
        self.auto_save = False  # No disk storage per security requirements
        
        # Processing settings
        self.parallel_processing = True
        self.chunk_size = 1000
        self.memory_limit_gb = 4
        
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI-specific configuration."""
        return {
            "title": self.app_title,
            "sidebar_width": 200,
            "max_content_width": 800,
            "dark_mode": self.dark_mode,
            "debug": self.show_debug_info
        }
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Get data processing configuration."""
        return {
            "parallel": self.parallel_processing,
            "chunk_size": self.chunk_size,
            "memory_limit": self.memory_limit_gb * 1024 * 1024 * 1024  # Convert to bytes
        }

# Global settings instance
settings = Settings()