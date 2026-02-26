"""
Phishing Simulation Platform - Configuration
"""

import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# ============================================================================
# DEPLOYMENT SETTINGS
# ============================================================================

# Environment (development, staging, production)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Base URL for tracking links
BASE_URL = os.getenv("BASE_URL", "https://sim.smecyberguard.com")
if ENVIRONMENT == "development":
    BASE_URL = "http://localhost:8000"

# ============================================================================
# EMAIL SETTINGS
# ============================================================================

# SMTP Configuration
SMTP_CONFIG = {
    "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", "587")),
    "username": os.getenv("SMTP_USERNAME", ""),
    "password": os.getenv("SMTP_PASSWORD", ""),
    "use_tls": True,
    "timeout": 30
}

# Email sending limits (prevent API rate limits)
EMAIL_LIMITS = {
    "batch_size": 50,  # Emails per batch
    "delay_between_batches": 60,  # Seconds
    "delay_between_emails": 2,  # Seconds
    "max_per_hour": 500
}

# ============================================================================
# DATABASE SETTINGS
# ============================================================================

# Local SQLite for simulation tracking
LOCAL_DB_PATH = os.getenv("LOCAL_DB", "./simulation_data.db")

# Turso integration (sync with SMEAgent)
TURSO_CONFIG = {
    "url": os.getenv("TURSO_URL", ""),
    "auth_token": os.getenv("TURSO_AUTH_TOKEN", ""),
    "sync_enabled": os.getenv("TURSO_SYNC", "true").lower() == "true",
    "sync_interval": 300  # Seconds (5 minutes)
}

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# Token generation
TOKEN_LENGTH = 32  # Length of tracking tokens
TOKEN_EXPIRY_DAYS = 30  # How long tokens are valid

# Rate limiting (prevent abuse)
RATE_LIMITS = {
    "api_requests_per_minute": 60,
    "clicks_per_ip_per_hour": 10
}

# ============================================================================
# CAMPAIGN SETTINGS
# ============================================================================

# Default campaign settings
DEFAULT_CAMPAIGN_CONFIG = {
    "from_name": "IT Security",
    "reply_to": "security@company.com",
    "track_opens": True,
    "track_clicks": True,
    "redirect_to_training": True,
    "send_reports": True
}

# Training redirect
TRAINING_URL = f"{BASE_URL}/training"

# Results notification
NOTIFICATION_EMAIL = os.getenv("ADMIN_EMAIL", "admin@smecyberguard.com")

# ============================================================================
# TEMPLATE SETTINGS
# ============================================================================

# Template categories
TEMPLATE_CATEGORIES = [
    "banking",
    "social_media",
    "ecommerce",
    "tech_support",
    "internal",
    "government",
    "custom"
]

# Template directory
TEMPLATES_DIR = "./templates"

# ============================================================================
# ANALYTICS SETTINGS
# ============================================================================

# Metrics to track
TRACKED_METRICS = [
    "emails_sent",
    "emails_delivered",
    "emails_opened",
    "links_clicked",
    "credentials_submitted",
    "training_completed"
]

# Risk scoring weights
RISK_SCORING = {
    "clicked_link": 10,
    "submitted_credentials": 25,
    "failed_training": 15,
    "repeat_offender": 20
}

# ============================================================================
# LOGGING
# ============================================================================

LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "./logs/simulation.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5
}

# ============================================================================
# INTEGRATION SETTINGS
# ============================================================================

# SMEAgent dashboard integration
SMEAGENT_API = {
    "url": os.getenv("SMEAGENT_API_URL", "https://dashboard.smecyberguard.com/api"),
    "api_key": os.getenv("SMEAGENT_API_KEY", ""),
    "sync_results": True
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    "enable_credential_capture": False,  # Never store real credentials
    "enable_email_opens_tracking": True,
    "enable_automated_campaigns": True,
    "enable_ab_testing": True,
    "enable_advanced_analytics": True,
    "enable_mobile_templates": True
}

# ============================================================================
# COMPLIANCE SETTINGS
# ============================================================================

COMPLIANCE = {
    "gdpr_compliant": True,
    "show_training_disclosure": True,
    "log_retention_days": 365,
    "anonymize_after_days": 90,
    "require_consent": False  # Part of employment security training
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_tracking_url(token: str) -> str:
    """Generate a tracking URL for a campaign"""
    return f"{BASE_URL}/track/{token}"

def get_training_url(token: str) -> str:
    """Generate training redirect URL"""
    return f"{BASE_URL}/training?source={token}"

def validate_config() -> bool:
    """Validate required configuration"""
    # In development mode, allow demo credentials
    if ENVIRONMENT == "development":
        # Accept demo credentials for development
        if SMTP_CONFIG["username"] and SMTP_CONFIG["password"] and BASE_URL:
            return True
    
    # For production, require real credentials
    required = [
        SMTP_CONFIG["username"],
        SMTP_CONFIG["password"],
        BASE_URL
    ]
    
    # Check for placeholder values
    placeholders = ["your-email", "your-app-password", "demo@"]
    if any(placeholder in str(val).lower() for val in required for placeholder in placeholders):
        if ENVIRONMENT != "development":
            print(f"⚠️  Using placeholder SMTP credentials in production mode")
            print(f"⚠️  Configure real SMTP settings in .env file")
            return False
    
    missing = [key for key in required if not key]
    
    if missing:
        print(f"⚠️  Missing required configuration")
        return False
    
    return True

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "ENVIRONMENT",
    "BASE_URL",
    "SMTP_CONFIG",
    "EMAIL_LIMITS",
    "LOCAL_DB_PATH",
    "TURSO_CONFIG",
    "DEFAULT_CAMPAIGN_CONFIG",
    "TRAINING_URL",
    "TEMPLATES_DIR",
    "TRACKED_METRICS",
    "RISK_SCORING",
    "LOG_CONFIG",
    "SMEAGENT_API",
    "FEATURES",
    "COMPLIANCE",
    "get_tracking_url",
    "get_training_url",
    "validate_config"
]
