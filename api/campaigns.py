"""
Campaign Management - Email sending and tracking
"""

import asyncio
import secrets
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
from pathlib import Path

import aiosmtplib
from jinja2 import Template
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SMTP_CONFIG, EMAIL_LIMITS, get_tracking_url
from models import Campaign, CampaignTarget

logger = logging.getLogger(__name__)


class CampaignManager:
    """Manage phishing simulation campaigns"""
    
    def __init__(self, db):
        self.db = db
        
    async def send_campaign(self, campaign_id: int):
        """Send all emails for a campaign"""
        
        logger.info(f"📧 Starting campaign: {campaign_id}")
        
        # Get campaign details
        campaign = await self.db.fetch_one(
            "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
        )
        
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Get template
        template = await self.db.fetch_one(
            "SELECT * FROM email_templates WHERE id = ?", (campaign["template_id"],)
        )
        
        if not template:
            raise ValueError(f"Template {campaign['template_id']} not found")
        
        # Get targets
        targets = await self.db.fetch_all(
            "SELECT * FROM campaign_targets WHERE campaign_id = ?", (campaign_id,)
        )
        
        logger.info(f"📬 Sending to {len(targets)} recipients")
        
        # Send emails in batches
        sent_count = 0
        failed_count = 0
        
        for i in range(0, len(targets), EMAIL_LIMITS["batch_size"]):
            batch = targets[i:i + EMAIL_LIMITS["batch_size"]]
            
            for target in batch:
                try:
                    await self._send_email(campaign, template, target)
                    
                    # Update target status
                    await self.db.execute(
                        "UPDATE campaign_targets SET sent_at = ? WHERE id = ?",
                        (datetime.now(), target["id"])
                    )
                    
                    sent_count += 1
                    logger.info(f"✅ Sent to {target['employee_email']} ({sent_count}/{len(targets)})")
                    
                    # Delay between emails
                    await asyncio.sleep(EMAIL_LIMITS["delay_between_emails"])
                    
                except Exception as e:
                    logger.error(f"❌ Failed to send to {target['employee_email']}: {e}")
                    failed_count += 1
            
            # Delay between batches
            if i + EMAIL_LIMITS["batch_size"] < len(targets):
                logger.info(f"⏸️  Batch complete. Waiting {EMAIL_LIMITS['delay_between_batches']}s...")
                await asyncio.sleep(EMAIL_LIMITS["delay_between_batches"])
        
        # Update campaign stats
        await self.db.execute(
            """UPDATE campaigns 
               SET status = 'active', 
                   sent_at = ?, 
                   emails_sent = ?,
                   emails_delivered = ?
               WHERE id = ?""",
            (datetime.now(), sent_count, sent_count, campaign_id)
        )
        
        logger.info(f"✅ Campaign complete: Sent {sent_count}, Failed {failed_count}")
        
        return {
            "campaign_id": campaign_id,
            "sent": sent_count,
            "failed": failed_count,
            "total": len(targets)
        }
    
    async def _send_email(self, campaign: Dict, template: Dict, target: Dict):
        """Send a single phishing email"""
        
        # Create tracking URL
        tracking_url = get_tracking_url(target["tracking_token"])
        
        # Render template
        html_content = self._render_template(
            template["html_body"],
            {
                "TRACKING_URL": tracking_url,
                "NAME": target["employee_name"],
                "EMAIL": target["employee_email"],
                "DATE": datetime.now().strftime("%B %d, %Y"),
                "TIME": datetime.now().strftime("%I:%M %p"),
                "DATE_TIME": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                "YEAR": datetime.now().year,
                "TRACKING_NUMBER": secrets.token_hex(8).upper(),
                "DEADLINE": "December 31, 2025",
                "EMPLOYEE_NAME": target["employee_name"]
            }
        )
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = campaign["subject"]
        message["From"] = f"{campaign['from_name']} <{campaign['from_email']}>"
        message["To"] = target["employee_email"]
        message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        
        # Add HTML part
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send via SMTP
        try:
            async with aiosmtplib.SMTP(
                hostname=SMTP_CONFIG["server"],
                port=SMTP_CONFIG["port"],
                use_tls=SMTP_CONFIG["use_tls"],
                timeout=SMTP_CONFIG["timeout"]
            ) as smtp:
                await smtp.login(
                    SMTP_CONFIG["username"],
                    SMTP_CONFIG["password"]
                )
                await smtp.send_message(message)
                
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            raise
    
    def _render_template(self, html: str, variables: Dict) -> str:
        """Render email template with variables"""
        template = Template(html)
        return template.render(**variables)


class TemplateLoader:
    """Load email templates from files"""
    
    def __init__(self, templates_dir: str = "./templates"):
        self.templates_dir = Path(templates_dir)
    
    async def load_templates(self, db):
        """Load all templates into database"""
        
        logger.info("📧 Loading email templates...")
        
        templates = [
            {
                "name": "KCB Bank - Suspicious Activity",
                "category": "banking",
                "difficulty": "medium",
                "description": "Fake bank security alert about suspicious login",
                "from_name": "KCB Bank Security",
                "from_email": "security@kcb-alerts.com",
                "subject": "URGENT: Suspicious Activity Detected on Your Account",
                "file": "banking/kcb_suspicious_activity.html"
            },
            {
                "name": "M-Pesa Verification",
                "category": "banking",
                "difficulty": "hard",
                "description": "Fake Safaricom M-Pesa account verification request",
                "from_name": "Safaricom M-Pesa",
                "from_email": "noreply@safaricom-mpesa.com",
                "subject": "M-Pesa Account Verification Required",
                "file": "banking/mpesa_verification.html"
            },
            {
                "name": "Facebook Security Alert",
                "category": "social_media",
                "difficulty": "easy",
                "description": "Fake Facebook login notification",
                "from_name": "Facebook",
                "from_email": "security@facebookmail.com",
                "subject": "Your account was logged in from a new device",
                "file": "social/facebook_security_alert.html"
            },
            {
                "name": "IT Password Reset",
                "category": "internal",
                "difficulty": "hard",
                "description": "Fake IT department mandatory password reset",
                "from_name": "IT Support",
                "from_email": "itsupport@company.com",
                "subject": "URGENT: Mandatory Password Reset Required",
                "file": "internal/password_reset_required.html"
            },
            {
                "name": "DHL Package Delivery",
                "category": "ecommerce",
                "difficulty": "medium",
                "description": "Fake package delivery failure notification",
                "from_name": "DHL Express",
                "from_email": "noreply@dhl-express.com",
                "subject": "Your Package Delivery Failed - Action Required",
                "file": "ecommerce/package_delivery_failed.html"
            }
        ]
        
        loaded = 0
        
        for template_info in templates:
            try:
                # Load HTML file
                file_path = self.templates_dir / template_info["file"]
                if file_path.exists():
                    html_body = file_path.read_text()
                else:
                    logger.warning(f"Template file not found: {file_path}")
                    html_body = "<p>Template content</p>"
                
                # Insert into database (check if exists first)
                existing = await db.fetch_one(
                    "SELECT id FROM email_templates WHERE name = ?",
                    (template_info["name"],)
                )
                
                if not existing:
                    await db.execute(
                        """INSERT INTO email_templates 
                           (name, category, difficulty, description, from_name, from_email, 
                            subject, html_body, text_body)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            template_info["name"],
                            template_info["category"],
                            template_info["difficulty"],
                            template_info["description"],
                            template_info["from_name"],
                            template_info["from_email"],
                            template_info["subject"],
                            html_body,
                            "Plain text version"  # TODO: Generate from HTML
                        )
                    )
                    loaded += 1
                    logger.info(f"✅ Loaded: {template_info['name']}")
                
            except Exception as e:
                logger.error(f"❌ Failed to load {template_info['name']}: {e}")
        
        logger.info(f"📧 Loaded {loaded} templates")


# Convenience function
async def load_default_templates(db):
    """Load default templates"""
    loader = TemplateLoader()
    await loader.load_templates(db)
