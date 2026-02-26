#!/usr/bin/env python3
"""
Phishing Simulation CLI Tool
Manage campaigns from the command line
"""

import asyncio
import sys
import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.progress import track

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api.app import db, Database
from api.campaigns import CampaignManager, TemplateLoader
from api.analytics import AnalyticsEngine
from api.models import CreateCampaignRequest
from config import validate_config

console = Console()


@click.group()
def cli():
    """🎣 Phishing Simulation Platform CLI"""
    pass


@cli.command()
def init():
    """Initialize database and load templates"""
    
    console.print("🚀 Initializing Phishing Simulation Platform...\n", style="bold green")
    
    async def _init():
        # Validate config
        if not validate_config():
            console.print("❌ Configuration invalid. Check config.py", style="bold red")
            return
        
        # Initialize database
        console.print("📊 Setting up database...")
        await db.connect()
        
        # Load templates
        console.print("📧 Loading email templates...")
        loader = TemplateLoader()
        await loader.load_templates(db)
        
        await db.close()
        
        console.print("\n✅ Initialization complete!", style="bold green")
        console.print("\nNext steps:", style="bold")
        console.print("  1. python cli.py templates list")
        console.print("  2. python cli.py campaign create")
        console.print("  3. python cli.py server start")
    
    asyncio.run(_init())


@cli.group()
def templates():
    """Manage email templates"""
    pass


@templates.command("list")
@click.option("--category", help="Filter by category")
def list_templates(category):
    """List available templates"""
    
    async def _list():
        await db.connect()
        
        if category:
            rows = await db.fetch_all(
                "SELECT * FROM email_templates WHERE category = ? ORDER BY name",
                (category,)
            )
        else:
            rows = await db.fetch_all(
                "SELECT * FROM email_templates ORDER BY category, name"
            )
        
        await db.close()
        
        if not rows:
            console.print("📧 No templates found", style="yellow")
            return
        
        table = Table(title="📧 Email Templates")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Category", style="magenta")
        table.add_column("Difficulty", style="yellow")
        table.add_column("Subject", style="white")
        
        for row in rows:
            table.add_row(
                str(row["id"]),
                row["name"],
                row["category"],
                row["difficulty"],
                row["subject"][:50] + "..." if len(row["subject"]) > 50 else row["subject"]
            )
        
        console.print(table)
        console.print(f"\n📊 Total: {len(rows)} templates")
    
    asyncio.run(_list())


@cli.group()
def campaign():
    """Manage campaigns"""
    pass


@campaign.command("create")
@click.option("--name", prompt="Campaign name", help="Name for this campaign")
@click.option("--business-id", prompt="Business ID", help="Business identifier")
@click.option("--template-id", prompt="Template ID", type=int, help="Template to use")
@click.option("--targets", prompt="Target emails (comma-separated)", help="Email addresses")
def create_campaign(name, business_id, template_id, targets):
    """Create a new campaign"""
    
    emails = [e.strip() for e in targets.split(",")]
    
    console.print(f"\n📧 Creating campaign: {name}", style="bold green")
    console.print(f"   Business: {business_id}")
    console.print(f"   Template: #{template_id}")
    console.print(f"   Targets: {len(emails)}")
    
    async def _create():
        await db.connect()
        
        # Verify template exists
        template = await db.fetch_one(
            "SELECT * FROM email_templates WHERE id = ?", (template_id,)
        )
        
        if not template:
            console.print(f"❌ Template #{template_id} not found", style="bold red")
            await db.close()
            return
        
        # Create campaign
        import secrets
        campaign_id = await db.execute(
            """INSERT INTO campaigns 
               (business_id, name, template_id, from_name, from_email, subject, 
                status, created_by, total_targets)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (business_id, name, str(template_id),
             template["from_name"], template["from_email"], template["subject"],
             "draft", "admin", len(emails))
        )
        
        # Create targets
        for email in track(emails, description="Adding targets..."):
            token = secrets.token_urlsafe(32)
            await db.execute(
                """INSERT INTO campaign_targets 
                   (campaign_id, employee_email, employee_name, tracking_token)
                   VALUES (?, ?, ?, ?)""",
                (campaign_id, email, email.split('@')[0], token)
            )
        
        await db.close()
        
        console.print(f"\n✅ Campaign created: ID {campaign_id}", style="bold green")
        console.print(f"\nNext: python cli.py campaign launch {campaign_id}")
    
    asyncio.run(_create())


@campaign.command("list")
@click.option("--business-id", help="Filter by business ID")
def list_campaigns(business_id):
    """List campaigns"""
    
    async def _list():
        await db.connect()
        
        if business_id:
            rows = await db.fetch_all(
                "SELECT * FROM campaigns WHERE business_id = ? ORDER BY created_at DESC",
                (business_id,)
            )
        else:
            rows = await db.fetch_all(
                "SELECT * FROM campaigns ORDER BY created_at DESC"
            )
        
        await db.close()
        
        if not rows:
            console.print("📧 No campaigns found", style="yellow")
            return
        
        table = Table(title="📧 Campaigns")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Targets", justify="right", style="magenta")
        table.add_column("Sent", justify="right", style="blue")
        table.add_column("Clicked", justify="right", style="red")
        
        for row in rows:
            click_rate = f"{(row['links_clicked']/row['emails_sent']*100):.1f}%" if row['emails_sent'] > 0 else "0%"
            table.add_row(
                str(row["id"]),
                row["name"],
                row["status"],
                str(row["total_targets"]),
                str(row["emails_sent"]),
                f"{row['links_clicked']} ({click_rate})"
            )
        
        console.print(table)
    
    asyncio.run(_list())


@campaign.command("launch")
@click.argument("campaign_id", type=int)
def launch_campaign(campaign_id):
    """Launch a campaign (send emails)"""
    
    console.print(f"🚀 Launching campaign #{campaign_id}...\n", style="bold green")
    
    async def _launch():
        await db.connect()
        
        manager = CampaignManager(db)
        
        try:
            result = await manager.send_campaign(campaign_id)
            
            console.print("\n✅ Campaign launched!", style="bold green")
            console.print(f"   Sent: {result['sent']}")
            console.print(f"   Failed: {result['failed']}")
            console.print(f"   Total: {result['total']}")
            
        except Exception as e:
            console.print(f"\n❌ Error: {e}", style="bold red")
        
        await db.close()
    
    asyncio.run(_launch())


@campaign.command("results")
@click.argument("campaign_id", type=int)
def campaign_results(campaign_id):
    """View campaign results"""
    
    async def _results():
        await db.connect()
        
        # Get campaign
        campaign = await db.fetch_one(
            "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
        )
        
        if not campaign:
            console.print(f"❌ Campaign #{campaign_id} not found", style="bold red")
            await db.close()
            return
        
        # Get analytics
        analytics = AnalyticsEngine(db)
        stats = await analytics.get_campaign_analytics(campaign_id)
        
        await db.close()
        
        console.print(f"\n📊 Campaign Results: {campaign['name']}\n", style="bold green")
        
        table = Table(show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Status", campaign["status"])
        table.add_row("Emails Sent", str(stats.total_sent))
        table.add_row("Delivered", f"{stats.total_delivered} ({stats.delivery_rate}%)")
        table.add_row("Opened", f"{stats.total_opened} ({stats.open_rate}%)")
        table.add_row("Clicked", f"{stats.total_clicked} ({stats.click_rate}%)")
        table.add_row("Submitted Credentials", f"{stats.total_submitted} ({stats.submission_rate}%)")
        table.add_row("Completed Training", f"{stats.total_trained} ({stats.training_rate}%)")
        
        if stats.avg_time_to_click:
            table.add_row("Avg Time to Click", f"{stats.avg_time_to_click:.1f} minutes")
        
        console.print(table)
    
    asyncio.run(_results())


@cli.group()
def server():
    """Server management"""
    pass


@server.command("start")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
def start_server(host, port):
    """Start the API server"""
    
    import uvicorn
    
    console.print("🚀 Starting Phishing Simulation API...\n", style="bold green")
    console.print(f"   Dashboard: http://{host}:{port}/dashboard")
    console.print(f"   API Docs: http://{host}:{port}/docs\n")
    
    uvicorn.run(
        "api.app:app",
        host=host,
        port=port,
        reload=True
    )


if __name__ == "__main__":
    cli()
