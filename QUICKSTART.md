# Quick Start Guide - Phishing Simulation Platform

## 📦 Installation

### 1. Install Dependencies

```bash
cd simulation
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your SMTP settings
nano .env
```

**Required settings:**
- `SMTP_SERVER` - Your SMTP server (e.g., smtp.gmail.com)
- `SMTP_USERNAME` - Your email address
- `SMTP_PASSWORD` - Your email password or app password
- `BASE_URL` - Where your platform is hosted

### 3. Initialize Database

```bash
python cli.py init
```

This will:
- Create the SQLite database
- Load default email templates
- Set up analytics tables

## 🚀 Quick Test

### List Available Templates

```bash
python cli.py templates list
```

Example output:
```
📧 Email Templates
┌────┬───────────────────────────┬──────────────┬────────────┐
│ ID │ Name                      │ Category     │ Difficulty │
├────┼───────────────────────────┼──────────────┼────────────┤
│ 1  │ KCB Bank - Suspicious...  │ banking      │ medium     │
│ 2  │ M-Pesa Verification       │ banking      │ hard       │
│ 3  │ Facebook Security Alert   │ social_media │ easy       │
└────┴───────────────────────────┴──────────────┴────────────┘
```

### Create a Test Campaign

```bash
python cli.py campaign create \
  --name "Q1 Security Training" \
  --business-id "test-business" \
  --template-id 1 \
  --targets "employee1@company.com,employee2@company.com"
```

### Launch Campaign

```bash
# Get campaign ID from previous command
python cli.py campaign launch 1
```

### View Results

```bash
python cli.py campaign results 1
```

## 🌐 Web Interface

### Start API Server

```bash
python cli.py server start
```

or

```bash
cd api
python app.py
```

### Access Dashboard

Open browser: `http://localhost:8000/dashboard`

### API Documentation

Automatic interactive API docs: `http://localhost:8000/docs`

## 📊 Example Workflow

### Complete Campaign Lifecycle

```bash
# 1. Initialize
python cli.py init

# 2. Browse templates
python cli.py templates list

# 3. Create campaign
python cli.py campaign create \
  --name "Monthly Phishing Test" \
  --business-id "acme-corp" \
  --template-id 2 \
  --targets "team@company.com"

# 4. Launch immediately
python cli.py campaign launch 1

# 5. Wait for clicks...

# 6. View results
python cli.py campaign results 1

# 7. Get employee risk profiles
# (via API or dashboard)
```

## 🔧 Configuration

### SMTP Setup (Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password:
   - Google Account → Security → App passwords
3. Use app password in `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### Using Other Email Services

**SendGrid:**
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**AWS SES:**
```env
SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your-ses-smtp-username
SMTP_PASSWORD=your-ses-smtp-password
```

## 📧 Email Templates

### Categories

- **banking** - Bank alerts, M-Pesa, financial services
- **social_media** - Facebook, LinkedIn, Instagram
- **ecommerce** - Amazon, delivery notifications
- **internal** - IT department, HR updates
- **tech_support** - Microsoft, Google, Apple

### Browse by Category

```bash
python cli.py templates list --category banking
```

## 🎯 API Usage

### Create Campaign via API

```bash
curl -X POST http://localhost:8000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "test-business",
    "name": "Security Training Q1",
    "template_id": "1",
    "target_emails": [
      "employee1@company.com",
      "employee2@company.com"
    ]
  }'
```

### Get Campaign Results

```bash
curl http://localhost:8000/api/campaigns/1
```

### Get Business Analytics

```bash
curl http://localhost:8000/api/analytics/business/test-business
```

## 🔍 Monitoring

### Check Logs

```bash
tail -f logs/simulation.log
```

### Monitor Database

```bash
sqlite3 simulation_data.db "SELECT * FROM campaigns;"
```

## 🐛 Troubleshooting

### SMTP Connection Errors

```
Error: Connection refused
```

**Solution:**
- Check firewall allows outbound SMTP (port 587)
- Verify SMTP credentials
- Check if SMTP server requires app password

### No Templates Loaded

```
📧 No templates found
```

**Solution:**
```bash
python cli.py init
```

### Campaign Not Sending

**Check:**
1. Campaign status: `python cli.py campaign list`
2. SMTP configuration in `.env`
3. Email limits not exceeded
4. Logs: `tail logs/simulation.log`

## 📚 Next Steps

### Integration with SMEAgent

1. Configure Turso sync in `.env`
2. Results automatically appear in SMEAgent dashboard
3. Risk scores feed into business security metrics

### Custom Templates

1. Copy existing template in `templates/`
2. Modify HTML
3. Add to database:
   ```bash
   # TODO: Add template import command
   ```

### Scheduled Campaigns

Use the API with a scheduler (cron, systemd timer):

```bash
# Create campaign
CAMPAIGN_ID=$(curl -s -X POST ... | jq -r '.id')

# Launch campaign
curl -X POST http://localhost:8000/api/campaigns/$CAMPAIGN_ID/launch
```

## 🆘 Support

- **Documentation:** `README.md`
- **API Docs:** http://localhost:8000/docs
- **Issues:** Contact SME CyberGuard support

---

**Ready to test your team's security awareness! 🎣**
