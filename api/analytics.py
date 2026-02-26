"""
Analytics and Risk Assessment
Track campaign results and employee risk profiles
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    CampaignAnalytics, EmployeeRiskProfile, BusinessAnalytics
)

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Calculate campaign analytics and risk scores"""
    
    def __init__(self, db):
        self.db = db
    
    async def get_campaign_analytics(self, campaign_id: int) -> CampaignAnalytics:
        """Get detailed analytics for a campaign"""
        
        campaign = await self.db.fetch_one(
            "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
        )
        
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Get target statistics
        stats = await self.db.fetch_one(
            """SELECT 
                   COUNT(*) as total_sent,
                   COUNT(CASE WHEN delivered_at IS NOT NULL THEN 1 END) as delivered,
                   COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END) as opened,
                   COUNT(CASE WHEN clicked_at IS NOT NULL THEN 1 END) as clicked,
                   COUNT(CASE WHEN submitted_at IS NOT NULL THEN 1 END) as submitted,
                   COUNT(CASE WHEN training_completed_at IS NOT NULL THEN 1 END) as trained
               FROM campaign_targets
               WHERE campaign_id = ?""",
            (campaign_id,)
        )
        
        # Calculate rates
        total = stats["total_sent"] or 1
        delivered = stats["delivered"] or stats["total_sent"]
        
        delivery_rate = (delivered / total) * 100
        open_rate = (stats["opened"] / delivered) * 100 if delivered > 0 else 0
        click_rate = (stats["clicked"] / delivered) * 100 if delivered > 0 else 0
        submission_rate = (stats["submitted"] / stats["clicked"]) * 100 if stats["clicked"] > 0 else 0
        training_rate = (stats["trained"] / stats["clicked"]) * 100 if stats["clicked"] > 0 else 0
        
        # Calculate time metrics
        time_stats = await self.db.fetch_one(
            """SELECT 
                   AVG((julianday(clicked_at) - julianday(sent_at)) * 24 * 60) as avg_time_to_click
               FROM campaign_targets
               WHERE campaign_id = ? AND clicked_at IS NOT NULL AND sent_at IS NOT NULL""",
            (campaign_id,)
        )
        
        return CampaignAnalytics(
            campaign_id=campaign_id,
            campaign_name=campaign["name"],
            total_sent=stats["total_sent"],
            total_delivered=delivered,
            delivery_rate=round(delivery_rate, 2),
            total_opened=stats["opened"],
            total_clicked=stats["clicked"],
            open_rate=round(open_rate, 2),
            click_rate=round(click_rate, 2),
            total_submitted=stats["submitted"],
            submission_rate=round(submission_rate, 2),
            total_trained=stats["trained"],
            training_rate=round(training_rate, 2),
            avg_time_to_click=round(time_stats["avg_time_to_click"], 1) if time_stats["avg_time_to_click"] else None,
            high_risk_employees=0,  # TODO: Calculate
            repeat_offenders=0,
            improvement_rate=0.0
        )
    
    async def get_employee_risk_profile(self, email: str, business_id: str) -> EmployeeRiskProfile:
        """Calculate risk profile for an employee"""
        
        # Get employee's campaign history
        stats = await self.db.fetch_one(
            """SELECT 
                   COUNT(DISTINCT ct.campaign_id) as campaigns_received,
                   COUNT(CASE WHEN ct.clicked_at IS NOT NULL THEN 1 END) as campaigns_clicked,
                   SUM(CASE WHEN cs.id IS NOT NULL THEN 1 END) as credentials_submitted,
                   COUNT(CASE WHEN ct.training_completed_at IS NOT NULL THEN 1 END) as trainings_completed,
                   MAX(ct.clicked_at) as last_clicked
               FROM campaign_targets ct
               LEFT JOIN credential_submissions cs ON ct.id = cs.target_id
               INNER JOIN campaigns c ON ct.campaign_id = c.id
               WHERE ct.employee_email = ? AND c.business_id = ?""",
            (email, business_id)
        )
        
        if not stats or stats["campaigns_received"] == 0:
            # New employee, no data
            return EmployeeRiskProfile(
                employee_email=email,
                employee_name=email.split('@')[0],
                campaigns_received=0,
                campaigns_clicked=0,
                credentials_submitted=0,
                trainings_completed=0,
                click_rate=0.0,
                submission_rate=0.0,
                training_completion_rate=0.0,
                risk_score=50,  # Neutral/unknown
                risk_level="unknown",
                days_since_last_incident=9999,
                improving=True,
                needs_additional_training=False,
                recommended_actions=["Complete initial security awareness training"]
            )
        
        # Calculate metrics
        click_rate = (stats["campaigns_clicked"] / stats["campaigns_received"]) * 100
        submission_rate = (stats["credentials_submitted"] / stats["campaigns_clicked"]) * 100 if stats["campaigns_clicked"] > 0 else 0
        training_rate = (stats["trainings_completed"] / stats["campaigns_clicked"]) * 100 if stats["campaigns_clicked"] > 0 else 0
        
        # Calculate risk score (0-100, higher = more risky)
        risk_score = 0
        risk_score += min(click_rate * 0.5, 50)  # Click rate (max 50 points)
        risk_score += min(submission_rate * 0.3, 30)  # Submission rate (max 30 points)
        risk_score += max(20 - (training_rate * 0.2), 0)  # Training completion (max 20 points penalty)
        
        # Determine risk level
        if risk_score < 20:
            risk_level = "low"
        elif risk_score < 40:
            risk_level = "medium"
        elif risk_score < 70:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        # Days since last incident
        days_since = 9999
        if stats["last_clicked"]:
            last_clicked = datetime.fromisoformat(stats["last_clicked"])
            days_since = (datetime.now() - last_clicked).days
        
        # Improvement trend (compare recent vs older campaigns)
        improving = await self._check_improvement_trend(email, business_id)
        
        # Recommendations
        recommendations = []
        if risk_level in ["high", "critical"]:
            recommendations.append("Schedule one-on-one security training session")
        if submission_rate > 20:
            recommendations.append("Immediate password reset required")
            recommendations.append("Enable multi-factor authentication")
        if training_rate < 50:
            recommendations.append("Complete mandatory security awareness modules")
        if stats["campaigns_clicked"] > 3:
            recommendations.append("May require additional monitoring")
        
        return EmployeeRiskProfile(
            employee_email=email,
            employee_name=email.split('@')[0],
            campaigns_received=stats["campaigns_received"],
            campaigns_clicked=stats["campaigns_clicked"],
            credentials_submitted=stats["credentials_submitted"],
            trainings_completed=stats["trainings_completed"],
            click_rate=round(click_rate, 2),
            submission_rate=round(submission_rate, 2),
            training_completion_rate=round(training_rate, 2),
            risk_score=int(risk_score),
            risk_level=risk_level,
            days_since_last_incident=days_since,
            improving=improving,
            needs_additional_training=risk_level in ["high", "critical"] or training_rate < 60,
            recommended_actions=recommendations
        )
    
    async def get_business_analytics(
        self, 
        business_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> BusinessAnalytics:
        """Get overall analytics for a business"""
        
        # Default to last 90 days
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=90)
        
        # Get campaign statistics
        campaign_stats = await self.db.fetch_one(
            """SELECT 
                   COUNT(*) as total_campaigns,
                   COUNT(CASE WHEN status = 'active' THEN 1 END) as active_campaigns,
                   COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_campaigns
               FROM campaigns
               WHERE business_id = ?
               AND created_at BETWEEN ? AND ?""",
            (business_id, start_date.isoformat(), end_date.isoformat())
        )
        
        # Get employee metrics
        employee_stats = await self.db.fetch_one(
            """SELECT 
                   COUNT(DISTINCT ct.employee_email) as total_employees,
                   COUNT(DISTINCT CASE WHEN ct.training_completed_at IS NOT NULL THEN ct.employee_email END) as trained,
                   COUNT(DISTINCT CASE WHEN ct.clicked_at IS NOT NULL THEN ct.employee_email END) as clicked
               FROM campaign_targets ct
               INNER JOIN campaigns c ON ct.campaign_id = c.id
               WHERE c.business_id = ?
               AND c.created_at BETWEEN ? AND ?""",
            (business_id, start_date.isoformat(), end_date.isoformat())
        )
        
        # Get high risk employees
        # (employees who clicked >50% of campaigns)
        high_risk_count = 0  # TODO: Implement proper calculation
        
        # Calculate overall click rate
        click_stats = await self.db.fetch_one(
            """SELECT 
                   COUNT(*) as total_sent,
                   COUNT(CASE WHEN clicked_at IS NOT NULL THEN 1 END) as total_clicked,
                   COUNT(CASE WHEN submitted_at IS NOT NULL THEN 1 END) as total_submitted,
                   COUNT(CASE WHEN training_completed_at IS NOT NULL THEN 1 END) as total_trained
               FROM campaign_targets ct
               INNER JOIN campaigns c ON ct.campaign_id = c.id
               WHERE c.business_id = ?
               AND c.created_at BETWEEN ? AND ?""",
            (business_id, start_date.isoformat(), end_date.isoformat())
        )
        
        total_sent = click_stats["total_sent"] or 1
        click_rate = (click_stats["total_clicked"] / total_sent) * 100
        submission_rate = (click_stats["total_submitted"] / click_stats["total_clicked"]) * 100 if click_stats["total_clicked"] > 0 else 0
        training_rate = (click_stats["total_trained"] / click_stats["total_clicked"]) * 100 if click_stats["total_clicked"] > 0 else 0
        
        # Calculate security score (0-100, higher = better)
        security_score = 100 - min(click_rate, 100)
        
        # Determine trend
        # TODO: Compare with previous period
        trend = "improving" if click_rate < 30 else "stable" if click_rate < 50 else "declining"
        
        # Industry comparison
        industry_avg = 30.0  # Average phishing click rate
        if click_rate < industry_avg * 0.7:
            performance = "better"
        elif click_rate < industry_avg * 1.3:
            performance = "average"
        else:
            performance = "worse"
        
        return BusinessAnalytics(
            business_id=business_id,
            business_name=business_id,  # TODO: Get actual name
            total_campaigns=campaign_stats["total_campaigns"],
            active_campaigns=campaign_stats["active_campaigns"],
            completed_campaigns=campaign_stats["completed_campaigns"],
            total_employees=employee_stats["total_employees"],
            employees_trained=employee_stats["trained"],
            high_risk_employees=high_risk_count,
            overall_click_rate=round(click_rate, 2),
            overall_submission_rate=round(submission_rate, 2),
            overall_training_rate=round(training_rate, 2),
            security_score=int(security_score),
            click_rate_trend=trend,
            month_over_month_improvement=0.0,  # TODO: Calculate
            industry_avg_click_rate=industry_avg,
            performance_vs_industry=performance,
            period_start=start_date,
            period_end=end_date
        )
    
    async def _check_improvement_trend(self, email: str, business_id: str) -> bool:
        """Check if employee is improving over time"""
        
        # Get recent campaigns (last 5)
        recent = await self.db.fetch_all(
            """SELECT clicked_at
               FROM campaign_targets ct
               INNER JOIN campaigns c ON ct.campaign_id = c.id
               WHERE ct.employee_email = ? AND c.business_id = ?
               ORDER BY ct.sent_at DESC
               LIMIT 5""",
            (email, business_id)
        )
        
        if len(recent) < 3:
            return True  # Not enough data, assume improving
        
        # Count clicks in recent vs older
        recent_clicks = sum(1 for r in recent[:2] if r["clicked_at"])
        older_clicks = sum(1 for r in recent[2:] if r["clicked_at"])
        
        # Improving if fewer recent clicks
        return recent_clicks < older_clicks
