# SME CyberGuard - Phishing Simulation Platform

## 🎯 Overview

A comprehensive phishing simulation platform designed to test and train employees on recognizing phishing attacks. Part of the SME CyberGuard security suite.

## ✨ Features

### 📧 Email Campaigns
- **Pre-built templates** - 20+ realistic phishing scenarios
- **Customizable** - Edit subject lines, sender names, content
- **Scheduling** - Launch campaigns automatically
- **Target groups** - Send to specific departments or individuals

### 🎭 Simulation Scenarios

1. **Banking & Finance**
   - Fake bank alerts
   - PayPal verification
   - M-Pesa/mobile money scams
   
2. **Tech Support**
   - Microsoft alerts
   - Password reset requests
   - Account verification

3. **Social Media**
   - Facebook security warnings
   - LinkedIn profile views
   - Instagram verification

4. **E-commerce**
   - Amazon order confirmations
   - Package delivery failures
   - Refund notifications

5. **Internal Threats**
   - HR policy updates
   - Payroll system alerts
   - IT department requests

### 📊 Tracking & Analytics

- **Click tracking** - Who clicked the phishing link
- **Credential submission** - Who entered passwords (training mode)
- **Time to click** - Response time analysis
- **Risk scoring** - Identify high-risk employees
- **Improvement tracking** - Track learning progress over time

### 🎓 Training Integration

- **Instant feedback** - Users redirected to training after click
- **Reporting** - Detailed reports for management
- **Integration** - Syncs with SMEAgent dashboard

## 🏗️ Architecture

```
simulation/
├── api/                  # FastAPI backend
│   ├── app.py           # Main application
│   ├── models.py        # Database models
│   ├── campaigns.py     # Campaign management
│   └── tracking.py      # Click tracking
├── templates/           # Email templates
│   ├── banking/
│   ├── social/
│   ├── ecommerce/
│   └── internal/
├── dashboard/           # Web UI
│   ├── index.html       # Results dashboard
│   └── campaign.html    # Campaign creator
├── config.py            # Configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Installation

```bash
cd simulation
pip install -r requirements.txt
```

### Configuration

1. Edit `config.py`:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
BASE_URL = "https://sim.smecyberguard.com"
```

2. Initialize database:
```bash
python api/app.py --init-db
```

### Launch Campaign

```bash
# CLI mode
python api/campaigns.py --template banking_alert --targets employees.csv

# API mode
python api/app.py
# Then visit http://localhost:8000/dashboard
```

## 📧 How It Works

### 1. Create Campaign

Choose a template and customize:
- Subject line
- Sender name/email
- Target list
- Schedule time

### 2. Email Sent

Employees receive realistic phishing email with tracking link:
```
https://sim.smecyberguard.com/track/abc123
```

### 3. Track Clicks

When user clicks:
- Click recorded with timestamp
- User redirected to training page
- Manager receives alert

### 4. View Results

Dashboard shows:
- Click rate (%)
- Most vulnerable employees
- Campaign effectiveness
- Improvement over time

## 🔒 Security & Ethics

### Safety Features

✅ **No real harm** - All links lead to training pages  
✅ **Clear disclosure** - Users informed it's a test after click  
✅ **No actual phishing** - Credentials never stored  
✅ **Privacy protected** - Individual data only for training  
✅ **Management controlled** - Only authorized personnel  

### Compliance

- **GDPR compliant** - Legitimate interest (security training)
- **Employment law** - Part of cybersecurity policy
- **Transparency** - Employees informed about training program
- **Data protection** - Results stored securely

## 🎨 Template Examples

### Banking Alert
```
From: KCB Bank Security <security@kcb-alerts.com>
Subject: Urgent: Suspicious Activity on Your Account

Dear Customer,

We detected unusual activity on your account. Click here to verify:
[Verify My Account]

If you don't verify within 24 hours, your account will be suspended.

KCB Bank Security Team
```

### IT Department
```
From: IT Support <it.support@company.com>
Subject: Password Reset Required

Hello,

Due to a security update, all employees must reset their passwords.

Click here to update: [Reset Password]

IT Department
```

## 📊 Integration with SMEAgent

Results automatically sync to SMEAgent dashboard:

```sql
-- phishing_simulations table
CREATE TABLE phishing_simulations (
    id INTEGER PRIMARY KEY,
    business_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    employee_email TEXT NOT NULL,
    sent_at DATETIME NOT NULL,
    clicked_at DATETIME,
    submitted_credentials BOOLEAN DEFAULT 0,
    completed_training BOOLEAN DEFAULT 0
);
```

Dashboard shows:
- Employees who clicked phishing link
- Training completion status
- Risk trends over time

## 🎯 Success Metrics

### Before Training
- 45% click rate (average SME)
- 12% credential submission
- High phishing risk

### After 3 Months
- 15% click rate (improving)
- 3% credential submission
- Medium risk

### After 6 Months
- 5% click rate (target achieved)
- <1% credential submission
- Low risk

## 🔧 Advanced Features

### Custom Templates
Create your own templates:
```python
from api.campaigns import Template

template = Template(
    name="custom_alert",
    subject="Your custom subject",
    html=open("custom.html").read(),
    category="custom"
)
```

### A/B Testing
Test different phishing tactics:
```python
campaign = Campaign(
    variant_a="urgent_tone",
    variant_b="friendly_tone",
    split=50  # 50/50 split
)
```

### Scheduled Campaigns
Automatic recurring tests:
```python
schedule = {
    "frequency": "monthly",
    "day": 15,
    "time": "10:00",
    "randomize": True  # Random employees each time
}
```

## 📱 API Endpoints

```
POST   /api/campaigns              Create new campaign
GET    /api/campaigns              List campaigns
GET    /api/campaigns/{id}         Get campaign details
GET    /api/campaigns/{id}/results View results
POST   /api/track/{token}          Track click (auto)
GET    /api/analytics              Overall statistics
```

## 🎓 Training Resources

After clicking simulated phishing:

1. **Immediate feedback** - "This was a phishing test"
2. **Education** - Warning signs they missed
3. **Best practices** - How to identify phishing
4. **Resources** - Links to security training
5. **Quiz** - Test understanding

## 🤝 Contributing

This is part of SME CyberGuard enterprise platform.

## 📄 License

MIT License - For security awareness training only

## ⚠️ Disclaimer

This tool is for **authorized security training only**. Unauthorized use for actual phishing is illegal and unethical.

---

**Built with ❤️ for African SMEs**  
Protecting businesses one employee at a time.
