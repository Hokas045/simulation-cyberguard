"""
Phishing Simulation Platform - Main API
FastAPI application for managing phishing simulation campaigns
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    Campaign, CampaignTarget, EmailTemplate,
    CreateCampaignRequest, CampaignResponse, AnalyticsResponse,
    ClickEvent, SCHEMA_SQL
)
from config import LOCAL_DB_PATH, BASE_URL, LOG_CONFIG, validate_config

# Import demo modules
sys.path.insert(0, str(Path(__file__).parent))
from demo import router as demo_router
from outlook_demo import router as outlook_router

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=LOG_CONFIG["level"],
    format=LOG_CONFIG["format"]
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE
# ============================================================================

class Database:
    """SQLite database connection manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection = None
    
    async def connect(self):
        """Initialize database connection"""
        self._connection = await aiosqlite.connect(self.db_path)
        self._connection.row_factory = aiosqlite.Row
        await self.init_schema()
        logger.info(f"📊 Database connected: {self.db_path}")
    
    async def init_schema(self):
        """Create database schema"""
        async with self._connection.cursor() as cursor:
            await cursor.executescript(SCHEMA_SQL)
        await self._connection.commit()
        logger.info("✅ Database schema initialized")
    
    async def close(self):
        """Close database connection"""
        if self._connection:
            await self._connection.close()
            logger.info("📊 Database closed")
    
    async def execute(self, query: str, params: tuple = ()):
        """Execute a query"""
        async with self._connection.cursor() as cursor:
            await cursor.execute(query, params)
            await self._connection.commit()
            return cursor.lastrowid
    
    async def fetch_one(self, query: str, params: tuple = ()):
        """Fetch one row"""
        async with self._connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()
    
    async def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all rows"""
        async with self._connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()


# Global database instance
db = Database(LOCAL_DB_PATH)


# ============================================================================
# APP LIFECYCLE
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    
    # Startup
    logger.info("🚀 Starting Phishing Simulation Platform...")
    
    # Validate configuration
    if not validate_config():
        logger.error("❌ Invalid configuration - check config.py")
        raise RuntimeError("Invalid configuration")
    
    # Initialize database
    await db.connect()
    
    # Load default templates
    await load_default_templates()
    
    logger.info("✅ Application ready")
    logger.info(f"🌐 Base URL: {BASE_URL}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    await db.close()


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Phishing Simulation Platform",
    description="Security awareness training through phishing simulations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include demo routers
app.include_router(demo_router)
app.include_router(outlook_router)


# ============================================================================
# API ENDPOINTS - CAMPAIGNS
# ============================================================================

@app.get("/")
async def root():
    """API root"""
    return {
        "service": "Phishing Simulation Platform",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "demo": "/demo",
            "campaigns": "/api/campaigns",
            "templates": "/api/templates",
            "analytics": "/api/analytics",
            "tracking": "/track/{token}",
            "dashboard": "/dashboard"
        }
    }


@app.post("/api/campaigns", response_model=Campaign)
async def create_campaign(request: CreateCampaignRequest):
    """Create a new phishing simulation campaign"""
    
    logger.info(f"📧 Creating campaign: {request.name}")
    
    # Get template
    template = await get_template_by_id(request.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Use custom values or template defaults
    from_name = request.custom_from_name or template["from_name"]
    from_email = request.custom_from_email or template["from_email"]
    subject = request.custom_subject or template["subject"]
    
    # Insert campaign
    campaign_id = await db.execute(
        """INSERT INTO campaigns 
           (business_id, name, template_id, from_name, from_email, subject, 
            status, created_by, total_targets)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (request.business_id, request.name, request.template_id,
         from_name, from_email, subject, "draft", "admin", len(request.target_emails))
    )
    
    # Create targets
    import secrets
    for email in request.target_emails:
        token = secrets.token_urlsafe(32)
        await db.execute(
            """INSERT INTO campaign_targets 
               (campaign_id, employee_email, employee_name, tracking_token)
               VALUES (?, ?, ?, ?)""",
            (campaign_id, email, email.split('@')[0], token)
        )
    
    logger.info(f"✅ Campaign created: ID={campaign_id}, Targets={len(request.target_emails)}")
    
    # Return campaign
    campaign_row = await db.fetch_one(
        "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
    )
    return dict(campaign_row)


@app.get("/api/campaigns", response_model=List[Campaign])
async def list_campaigns(business_id: Optional[str] = None):
    """List all campaigns"""
    
    if business_id:
        rows = await db.fetch_all(
            "SELECT * FROM campaigns WHERE business_id = ? ORDER BY created_at DESC",
            (business_id,)
        )
    else:
        rows = await db.fetch_all(
            "SELECT * FROM campaigns ORDER BY created_at DESC"
        )
    
    return [dict(row) for row in rows]


@app.get("/api/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int):
    """Get campaign details with targets"""
    
    campaign_row = await db.fetch_one(
        "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
    )
    
    if not campaign_row:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    targets_rows = await db.fetch_all(
        "SELECT * FROM campaign_targets WHERE campaign_id = ?", (campaign_id,)
    )
    
    return {
        "campaign": dict(campaign_row),
        "targets": [dict(row) for row in targets_rows],
        "analytics": None  # TODO: Calculate analytics
    }


@app.post("/api/campaigns/{campaign_id}/launch")
async def launch_campaign(campaign_id: int):
    """Launch a campaign (send emails)"""
    
    logger.info(f"🚀 Launching campaign: {campaign_id}")
    
    # Update status
    await db.execute(
        "UPDATE campaigns SET status = ?, sent_at = ? WHERE id = ?",
        ("active", datetime.now(), campaign_id)
    )
    
    # TODO: Send emails in background task
    # For now, we'll mark as sent
    
    return {"status": "launched", "campaign_id": campaign_id}


# ============================================================================
# API ENDPOINTS - TEMPLATES
# ============================================================================

@app.get("/api/templates", response_model=List[dict])
async def list_templates(category: Optional[str] = None):
    """List available email templates"""
    
    if category:
        rows = await db.fetch_all(
            "SELECT * FROM email_templates WHERE category = ? ORDER BY name",
            (category,)
        )
    else:
        rows = await db.fetch_all(
            "SELECT * FROM email_templates ORDER BY category, name"
        )
    
    return [dict(row) for row in rows]


async def get_template_by_id(template_id: str):
    """Get template by ID"""
    return await db.fetch_one(
        "SELECT * FROM email_templates WHERE id = ?", (template_id,)
    )


# ============================================================================
# TRACKING ENDPOINTS
# ============================================================================

@app.get("/track/{token}")
async def track_click(token: str, request: Request):
    """Track phishing link click"""
    
    logger.info(f"🔗 Click tracked: {token}")
    
    # Find target
    target = await db.fetch_one(
        "SELECT * FROM campaign_targets WHERE tracking_token = ?", (token,)
    )
    
    if not target:
        raise HTTPException(status_code=404, detail="Invalid tracking token")
    
    # Record click event
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")
    
    await db.execute(
        """INSERT INTO click_events 
           (campaign_id, target_id, tracking_token, ip_address, user_agent)
           VALUES (?, ?, ?, ?, ?)""",
        (target["campaign_id"], target["id"], token, ip_address, user_agent)
    )
    
    # Update target
    await db.execute(
        """UPDATE campaign_targets 
           SET clicked_at = ?, ip_address = ?, user_agent = ?
           WHERE id = ?""",
        (datetime.now(), ip_address, user_agent, target["id"])
    )
    
    # Update campaign stats
    await db.execute(
        """UPDATE campaigns 
           SET links_clicked = links_clicked + 1
           WHERE id = ?""",
        (target["campaign_id"],)
    )
    
    # Redirect to training page
    return RedirectResponse(url=f"/training?token={token}")


@app.get("/training")
async def training_page(token: str):
    """Training/education page after click"""
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Awareness Training</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .warning {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 20px;
                margin: 20px 0;
            }
            .success {
                background: #d4edda;
                border-left: 4px solid #28a745;
                padding: 20px;
                margin: 20px 0;
            }
            h1 { color: #d9534f; }
            h2 { color: #333; }
            ul { line-height: 1.8; }
            .btn {
                display: inline-block;
                padding: 12px 30px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚠️ This Was A Phishing Simulation</h1>
            
            <div class="warning">
                <strong>You just clicked a simulated phishing link.</strong><br>
                This was a security awareness training exercise. Your action has been recorded for training purposes only.
            </div>
            
            <h2>🎓 What You Should Have Noticed:</h2>
            <ul>
                <li><strong>Suspicious sender:</strong> Check if the email address matches the claimed sender</li>
                <li><strong>Urgency tactics:</strong> Phishing emails often create false urgency</li>
                <li><strong>Suspicious links:</strong> Hover over links to see the real URL before clicking</li>
                <li><strong>Grammar errors:</strong> Many phishing emails contain spelling/grammar mistakes</li>
                <li><strong>Requests for credentials:</strong> Legitimate companies never ask for passwords via email</li>
            </ul>
            
            <h2>✅ What To Do Next Time:</h2>
            <ul>
                <li>Verify the sender's email address carefully</li>
                <li>Don't click links in unexpected emails</li>
                <li>Type URLs directly into your browser</li>
                <li>Report suspicious emails to IT/security team</li>
                <li>When in doubt, call the company directly using a known number</li>
            </ul>
            
            <div class="success">
                <strong>Learning is the goal!</strong><br>
                No actual harm was done. This training helps protect you and your organization from real phishing attacks.
            </div>
            
            <a href="https://dashboard.smecyberguard.com" class="btn">Return to Dashboard</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/business/{business_id}")
async def get_business_analytics(business_id: str):
    """Get analytics for a business"""
    
    # Get campaign stats
    stats = await db.fetch_one(
        """SELECT 
               COUNT(*) as total_campaigns,
               SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
               SUM(total_targets) as total_targets,
               SUM(links_clicked) as total_clicks,
               SUM(credentials_submitted) as total_submissions
           FROM campaigns
           WHERE business_id = ?""",
        (business_id,)
    )
    
    if not stats or stats["total_campaigns"] == 0:
        return {"message": "No campaigns yet"}
    
    click_rate = (stats["total_clicks"] / stats["total_targets"] * 100) if stats["total_targets"] > 0 else 0
    
    return {
        "business_id": business_id,
        "total_campaigns": stats["total_campaigns"],
        "active_campaigns": stats["active"],
        "total_targets": stats["total_targets"],
        "total_clicks": stats["total_clicks"],
        "click_rate": round(click_rate, 2),
        "security_score": max(0, 100 - int(click_rate))
    }


# ============================================================================
# DASHBOARD
# ============================================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Simple dashboard UI"""
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phishing Simulation Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f7fa;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .container {
                max-width: 1200px;
                margin: 30px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                border-radius: 10px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
            }
            .stat h3 { font-size: 36px; margin-bottom: 10px; }
            .stat p { opacity: 0.9; }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin: 10px 5px;
            }
            .btn:hover { background: #764ba2; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎣 Phishing Simulation Platform</h1>
            <p>Security Awareness Training Dashboard</p>
        </div>
        
        <div class="container">
            <div class="card">
                <h2>Quick Actions</h2>
                <a href="/outlook-demo" class="btn">🛡️ SMEAgent + Outlook Demo</a>
                <a href="/demo" class="btn">🎯 Live Attack Demo</a>
                <a href="/api/campaigns" class="btn">View Campaigns</a>
                <a href="/api/templates" class="btn">Browse Templates</a>
                <a href="/docs" class="btn">API Documentation</a>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <h3>0</h3>
                    <p>Active Campaigns</p>
                </div>
                <div class="stat">
                    <h3>20+</h3>
                    <p>Email Templates</p>
                </div>
                <div class="stat">
                    <h3>0</h3>
                    <p>Total Clicks</p>
                </div>
            </div>
            
            <div class="card">
                <h2>Getting Started</h2>
                <ol style="line-height: 2;">
                    <li>Configure SMTP settings in <code>config.py</code></li>
                    <li>Browse available templates at <code>/api/templates</code></li>
                    <li>Create a campaign via POST <code>/api/campaigns</code></li>
                    <li>Launch campaign with <code>/api/campaigns/{id}/launch</code></li>
                    <li>Monitor results in real-time</li>
                </ol>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


# ============================================================================
# UTILITIES
# ============================================================================

async def load_default_templates():
    """Load default email templates into database"""
    
    # Check if templates already loaded
    count_row = await db.fetch_one("SELECT COUNT(*) as count FROM email_templates")
    if count_row and count_row["count"] > 0:
        logger.info(f"📧 Templates already loaded: {count_row['count']}")
        return
    
    # Will be loaded from template files
    logger.info("📧 Default templates will be loaded from files")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("🎣 Starting Phishing Simulation Platform...")
    print(f"🌐 Dashboard: http://localhost:8000/dashboard")
    print(f"📚 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
