"""
Database Models for Phishing Simulation Platform
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# CAMPAIGN MODELS
# ============================================================================

class Campaign(BaseModel):
    """Phishing simulation campaign"""
    id: Optional[int] = None
    business_id: str
    name: str
    template_id: str
    from_name: str
    from_email: EmailStr
    subject: str
    status: str = "draft"  # draft, scheduled, active, completed, cancelled
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str  # user email or ID
    
    # Statistics (updated as campaign runs)
    total_targets: int = 0
    emails_sent: int = 0
    emails_delivered: int = 0
    emails_opened: int = 0
    links_clicked: int = 0
    credentials_submitted: int = 0
    training_completed: int = 0


class CampaignTarget(BaseModel):
    """Individual target in a campaign"""
    id: Optional[int] = None
    campaign_id: int
    employee_email: EmailStr
    employee_name: str
    department: Optional[str] = None
    tracking_token: str
    
    # Status tracking
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    training_completed_at: Optional[datetime] = None
    
    # Metadata
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None


# ============================================================================
# TEMPLATE MODELS
# ============================================================================

class EmailTemplate(BaseModel):
    """Phishing email template"""
    id: Optional[int] = None
    name: str
    category: str  # banking, social_media, ecommerce, tech_support, internal
    difficulty: str = "medium"  # easy, medium, hard, expert
    description: str
    
    # Email content
    from_name: str
    from_email: str
    subject: str
    html_body: str
    text_body: str
    
    # Configuration
    has_attachments: bool = False
    attachment_types: Optional[List[str]] = None
    uses_urgency: bool = False
    uses_authority: bool = False
    uses_scarcity: bool = False
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    times_used: int = 0
    avg_click_rate: float = 0.0


# ============================================================================
# TRACKING MODELS
# ============================================================================

class ClickEvent(BaseModel):
    """Individual click event"""
    id: Optional[int] = None
    campaign_id: int
    target_id: int
    tracking_token: str
    clicked_at: datetime = Field(default_factory=datetime.now)
    
    # Browser/device info
    ip_address: str
    user_agent: str
    browser: Optional[str] = None
    device_type: Optional[str] = None
    os: Optional[str] = None
    
    # Location (if available)
    country: Optional[str] = None
    city: Optional[str] = None


class CredentialSubmission(BaseModel):
    """Credential submission event (training only - never store actual credentials)"""
    id: Optional[int] = None
    campaign_id: int
    target_id: int
    tracking_token: str
    submitted_at: datetime = Field(default_factory=datetime.now)
    
    # What was submitted (for analytics, not actual values)
    submitted_username: bool = False
    submitted_password: bool = False
    submitted_credit_card: bool = False
    submitted_ssn: bool = False
    
    # Browser info
    ip_address: str
    user_agent: str


# ============================================================================
# ANALYTICS MODELS
# ============================================================================

class CampaignAnalytics(BaseModel):
    """Analytics for a campaign"""
    campaign_id: int
    campaign_name: str
    
    # Delivery metrics
    total_sent: int
    total_delivered: int
    delivery_rate: float
    
    # Engagement metrics
    total_opened: int
    total_clicked: int
    open_rate: float
    click_rate: float
    
    # Security metrics
    total_submitted: int
    submission_rate: float
    total_trained: int
    training_rate: float
    
    # Time metrics
    avg_time_to_open: Optional[float] = None  # Minutes
    avg_time_to_click: Optional[float] = None
    
    # Risk assessment
    high_risk_employees: int
    repeat_offenders: int
    improvement_rate: float


class EmployeeRiskProfile(BaseModel):
    """Risk profile for an employee"""
    employee_email: EmailStr
    employee_name: str
    department: Optional[str] = None
    
    # Historical data
    campaigns_received: int
    campaigns_clicked: int
    credentials_submitted: int
    trainings_completed: int
    
    # Risk metrics
    click_rate: float
    submission_rate: float
    training_completion_rate: float
    risk_score: int  # 0-100
    risk_level: str  # low, medium, high, critical
    
    # Trends
    last_clicked: Optional[datetime] = None
    days_since_last_incident: int
    improving: bool
    
    # Recommendations
    needs_additional_training: bool
    recommended_actions: List[str] = []


class BusinessAnalytics(BaseModel):
    """Overall analytics for a business"""
    business_id: str
    business_name: str
    
    # Campaign summary
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    
    # Employee metrics
    total_employees: int
    employees_trained: int
    high_risk_employees: int
    
    # Security posture
    overall_click_rate: float
    overall_submission_rate: float
    overall_training_rate: float
    security_score: int  # 0-100
    
    # Trends
    click_rate_trend: str  # improving, stable, declining
    month_over_month_improvement: float
    
    # Comparisons
    industry_avg_click_rate: float = 30.0
    performance_vs_industry: str  # better, average, worse
    
    # Time period
    period_start: datetime
    period_end: datetime


# ============================================================================
# TURSO SYNC MODELS (for SMEAgent integration)
# ============================================================================

class PhishingSimulationRecord(BaseModel):
    """Record to sync to Turso (matches SMEAgent schema)"""
    business_id: str
    campaign_id: str
    employee_email: str
    sent_at: datetime
    clicked_at: Optional[datetime] = None
    submitted_credentials: bool = False
    completed_training: bool = False
    synced_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateCampaignRequest(BaseModel):
    """Request to create a new campaign"""
    business_id: str
    name: str
    template_id: str
    target_emails: List[EmailStr]
    schedule_time: Optional[datetime] = None
    
    # Optional customizations
    custom_subject: Optional[str] = None
    custom_from_name: Optional[str] = None
    custom_from_email: Optional[EmailStr] = None


class CampaignResponse(BaseModel):
    """Response with campaign details"""
    campaign: Campaign
    targets: List[CampaignTarget]
    analytics: Optional[CampaignAnalytics] = None


class AnalyticsResponse(BaseModel):
    """Response with analytics data"""
    business: BusinessAnalytics
    campaigns: List[CampaignAnalytics]
    high_risk_employees: List[EmployeeRiskProfile]
    recommendations: List[str]


# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

SCHEMA_SQL = """
-- Campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id TEXT NOT NULL,
    name TEXT NOT NULL,
    template_id TEXT NOT NULL,
    from_name TEXT NOT NULL,
    from_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT DEFAULT 'draft',
    scheduled_at DATETIME,
    sent_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT NOT NULL,
    total_targets INTEGER DEFAULT 0,
    emails_sent INTEGER DEFAULT 0,
    emails_delivered INTEGER DEFAULT 0,
    emails_opened INTEGER DEFAULT 0,
    links_clicked INTEGER DEFAULT 0,
    credentials_submitted INTEGER DEFAULT 0,
    training_completed INTEGER DEFAULT 0
);

-- Campaign targets
CREATE TABLE IF NOT EXISTS campaign_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    employee_email TEXT NOT NULL,
    employee_name TEXT NOT NULL,
    department TEXT,
    tracking_token TEXT UNIQUE NOT NULL,
    sent_at DATETIME,
    delivered_at DATETIME,
    opened_at DATETIME,
    clicked_at DATETIME,
    submitted_at DATETIME,
    training_completed_at DATETIME,
    ip_address TEXT,
    user_agent TEXT,
    location TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Email templates
CREATE TABLE IF NOT EXISTS email_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT DEFAULT 'medium',
    description TEXT NOT NULL,
    from_name TEXT NOT NULL,
    from_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    html_body TEXT NOT NULL,
    text_body TEXT NOT NULL,
    has_attachments BOOLEAN DEFAULT 0,
    attachment_types TEXT,
    uses_urgency BOOLEAN DEFAULT 0,
    uses_authority BOOLEAN DEFAULT 0,
    uses_scarcity BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    times_used INTEGER DEFAULT 0,
    avg_click_rate REAL DEFAULT 0.0
);

-- Click events
CREATE TABLE IF NOT EXISTS click_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    tracking_token TEXT NOT NULL,
    clicked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    browser TEXT,
    device_type TEXT,
    os TEXT,
    country TEXT,
    city TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (target_id) REFERENCES campaign_targets(id)
);

-- Credential submissions
CREATE TABLE IF NOT EXISTS credential_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    tracking_token TEXT NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    submitted_username BOOLEAN DEFAULT 0,
    submitted_password BOOLEAN DEFAULT 0,
    submitted_credit_card BOOLEAN DEFAULT 0,
    submitted_ssn BOOLEAN DEFAULT 0,
    ip_address TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (target_id) REFERENCES campaign_targets(id)
);

-- Turso sync log
CREATE TABLE IF NOT EXISTS turso_sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    synced_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sync_status TEXT DEFAULT 'success',
    error_message TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (target_id) REFERENCES campaign_targets(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_campaigns_business ON campaigns(business_id);
CREATE INDEX IF NOT EXISTS idx_targets_campaign ON campaign_targets(campaign_id);
CREATE INDEX IF NOT EXISTS idx_targets_token ON campaign_targets(tracking_token);
CREATE INDEX IF NOT EXISTS idx_clicks_campaign ON click_events(campaign_id);
CREATE INDEX IF NOT EXISTS idx_clicks_target ON click_events(target_id);
CREATE INDEX IF NOT EXISTS idx_submissions_campaign ON credential_submissions(campaign_id);
"""
