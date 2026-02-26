"""
Interactive Phishing Attack Demo
Shows how a real-world phishing attack unfolds
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import secrets

router = APIRouter()


@router.get("/demo", response_class=HTMLResponse)
async def phishing_demo():
    """Interactive phishing attack simulation"""
    
    demo_token = secrets.token_urlsafe(16)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phishing Attack Simulation - Real World Demo</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 36px;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header p {
                font-size: 18px;
                opacity: 0.95;
            }
            
            .demo-stages {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stage {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            
            .stage:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            .stage-number {
                display: inline-block;
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 50%;
                text-align: center;
                line-height: 40px;
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 15px;
            }
            
            .stage h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 18px;
            }
            
            .stage p {
                color: #666;
                line-height: 1.6;
                font-size: 14px;
            }
            
            .inbox-container {
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            
            .inbox-header {
                background: linear-gradient(to right, #f5f5f5, #e8e8e8);
                padding: 20px;
                border-bottom: 2px solid #ddd;
            }
            
            .inbox-header h2 {
                color: #333;
                font-size: 24px;
            }
            
            .email-list {
                list-style: none;
            }
            
            .email-item {
                padding: 20px;
                border-bottom: 1px solid #eee;
                cursor: pointer;
                transition: all 0.2s;
                position: relative;
            }
            
            .email-item:hover {
                background: #f9f9f9;
                border-left: 5px solid #667eea;
            }
            
            .email-item.phishing {
                border-left: 4px solid #d9534f;
            }
            
            .email-item.phishing:hover {
                background: #fff5f5;
                border-left: 5px solid #d9534f;
            }
            
            .email-item.safe {
                border-left: 4px solid #5cb85c;
            }
            
            .email-item.safe:hover {
                border-left: 5px solid #5cb85c;
            }
            
            .email-sender {
                font-weight: 600;
                color: #333;
                margin-bottom: 8px;
                font-size: 15px;
            }
            
            .email-subject {
                color: #666;
                margin-bottom: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            
            .email-preview {
                color: #999;
                font-size: 13px;
                line-height: 1.4;
            }
            
            .email-time {
                position: absolute;
                right: 70px;
                top: 20px;
                color: #999;
                font-size: 12px;
            }
            
            .warning-badge {
                position: absolute;
                right: 20px;
                top: 50%;
                transform: translateY(-50%);
                background: #d9534f;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 11px;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(217, 83, 79, 0.3);
            }
            
            .safe-badge {
                position: absolute;
                right: 20px;
                top: 50%;
                transform: translateY(-50%);
                background: #5cb85c;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 11px;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(92, 184, 92, 0.3);
            }
            
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.85);
                z-index: 1000;
                align-items: center;
                justify-content: center;
                backdrop-filter: blur(5px);
            }
            
            .modal.active {
                display: flex;
            }
            
            .modal-content {
                background: white;
                border-radius: 10px;
                max-width: 900px;
                width: 95%;
                max-height: 95vh;
                overflow-y: auto;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateY(-50px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            .modal-header {
                padding: 20px 30px;
                border-bottom: 1px solid #ddd;
                background: #f8f9fa;
            }
            
            .modal-body {
                padding: 0;
            }
            
            .modal-footer {
                padding: 20px;
                border-top: 1px solid #ddd;
                text-align: right;
                background: #f8f9fa;
            }
            
            /* Fake bank login page styles */
            .fake-bank-page {
                background: #fff;
            }
            
            .bank-header {
                background: #1a1a1a;
                color: white;
                padding: 20px 30px;
                text-align: center;
            }
            
            .bank-logo {
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            
            .bank-alert {
                background: #d9534f;
                color: white;
                padding: 15px 30px;
                text-align: center;
                font-weight: 600;
            }
            
            .bank-form {
                padding: 40px 30px;
                max-width: 500px;
                margin: 0 auto;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
                font-size: 14px;
            }
            
            .form-group input {
                width: 100%;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 15px;
                transition: border-color 0.2s;
            }
            
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .btn {
                display: inline-block;
                padding: 12px 24px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                cursor: pointer;
                border: none;
                font-size: 16px;
                transition: all 0.2s;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                width: 100%;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
            
            .btn-danger {
                background: #d9534f;
                color: white;
                width: 100%;
                padding: 15px;
                font-size: 16px;
            }
            
            .btn-danger:hover {
                background: #c9302c;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(217, 83, 79, 0.4);
            }
            
            .btn-success {
                background: #00a651;
                color: white;
                width: 100%;
                padding: 15px;
                font-size: 16px;
            }
            
            .btn-close {
                background: #6c757d;
                color: white;
            }
            
            .btn-close:hover {
                background: #5a6268;
            }
            
            .warning-box {
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 30px;
            }
            
            .warning-box h3 {
                color: #856404;
                margin-bottom: 15px;
                font-size: 18px;
            }
            
            .warning-box ul {
                margin-left: 20px;
                color: #856404;
                line-height: 1.8;
            }
            
            .warning-box li {
                margin-bottom: 8px;
            }
            
            .captured-data {
                background: #f8d7da;
                border: 2px solid #dc3545;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 30px;
            }
            
            .captured-data h3 {
                color: #721c24;
                margin-bottom: 15px;
                font-size: 18px;
            }
            
            .data-item {
                background: white;
                padding: 12px 15px;
                margin: 8px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                color: #721c24;
                font-size: 13px;
            }
            
            .timeline {
                position: relative;
                padding-left: 40px;
                margin: 30px;
            }
            
            .timeline::before {
                content: '';
                position: absolute;
                left: 12px;
                top: 0;
                bottom: 0;
                width: 3px;
                background: linear-gradient(to bottom, #667eea, #764ba2);
            }
            
            .timeline-item {
                position: relative;
                margin-bottom: 30px;
            }
            
            .timeline-item::before {
                content: '';
                position: absolute;
                left: -34px;
                top: 5px;
                width: 18px;
                height: 18px;
                border-radius: 50%;
                background: #667eea;
                border: 4px solid white;
                box-shadow: 0 0 0 2px #667eea;
            }
            
            .timeline-item h4 {
                color: #333;
                margin-bottom: 8px;
                font-size: 16px;
            }
            
            .timeline-item p {
                color: #666;
                line-height: 1.6;
                font-size: 14px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            
            .stat-card {
                background: white;
                color: #333;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            .stat-card h3 {
                font-size: 42px;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .stat-card p {
                opacity: 0.8;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .success-box {
                background: #d4edda;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 30px;
            }
            
            .success-box h3 {
                color: #155724;
                margin-bottom: 15px;
                font-size: 18px;
            }
            
            .success-box p, .success-box ul {
                color: #155724;
                line-height: 1.7;
            }
            
            .success-box ul {
                margin-left: 20px;
                margin-top: 15px;
            }
            
            .success-box li {
                margin-bottom: 8px;
            }
            
            /* M-Pesa styling */
            .mpesa-header {
                background: #00a651;
                color: white;
                padding: 25px 30px;
                text-align: center;
            }
            
            .mpesa-logo {
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            
            .mpesa-tagline {
                font-size: 12px;
                opacity: 0.9;
                margin-top: 5px;
            }
            
            /* Loading animation */
            .loading {
                display: none;
                text-align: center;
                padding: 40px;
            }
            
            .loading.active {
                display: block;
            }
            
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .url-bar {
                background: #f8f9fa;
                padding: 15px 30px;
                border-bottom: 1px solid #ddd;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #666;
            }
            
            .url-bar .lock {
                color: #999;
                margin-right: 8px;
            }
            
            .url-bar .fake-url {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎣 Real-World Phishing Attack Simulation</h1>
                <p>Experience exactly how attackers trick victims and steal credentials</p>
            </div>
            
            <div class="demo-stages">
                <div class="stage">
                    <div class="stage-number">1</div>
                    <h3>📧 Phishing Email</h3>
                    <p>Realistic email that mimics legitimate companies with perfect branding and urgent language.</p>
                </div>
                
                <div class="stage">
                    <div class="stage-number">2</div>
                    <h3>🔗 Malicious Link</h3>
                    <p>Victim clicks link that appears safe but leads to fake website that looks identical to real one.</p>
                </div>
                
                <div class="stage">
                    <div class="stage-number">3</div>
                    <h3>💳 Fake Login Page</h3>
                    <p>Perfect replica of bank/service login. Victim enters real credentials thinking it's legitimate.</p>
                </div>
                
                <div class="stage">
                    <div class="stage-number">4</div>
                    <h3>💀 Account Takeover</h3>
                    <p>Attacker now has credentials, device info, and full access to victim's account and money.</p>
                </div>
            </div>
            
            <div class="inbox-container">
                <div class="inbox-header">
                    <h2>📧 Your Email Inbox - Click to Experience Real Phishing Attacks</h2>
                </div>
                
                <ul class="email-list">
                    <li class="email-item safe" onclick="showSafeEmail()">
                        <div class="email-time">10:15 AM</div>
                        <div class="email-sender">LinkedIn (notifications@linkedin.com)</div>
                        <div class="email-subject">John Smith viewed your profile</div>
                        <div class="email-preview">John Smith from Google viewed your LinkedIn profile. See who's been looking at your profile...</div>
                        <span class="safe-badge">✓ SAFE</span>
                    </li>
                    
                    <li class="email-item phishing" onclick="showPhishingEmail('banking')">
                        <div class="email-time">9:47 AM</div>
                        <div class="email-sender">KCB Bank Security (security@kcb-alerts.com)</div>
                        <div class="email-subject">⚠️ URGENT: Suspicious Activity Detected on Your Account</div>
                        <div class="email-preview">We detected unusual login attempts from Lagos, Nigeria. Verify immediately or account will be suspended...</div>
                        <span class="warning-badge">⚠️ PHISHING</span>
                    </li>
                    
                    <li class="email-item safe" onclick="showSafeEmail()">
                        <div class="email-time">Yesterday</div>
                        <div class="email-sender">Amazon.com (auto-confirm@amazon.com)</div>
                        <div class="email-subject">Your Amazon.com order has shipped</div>
                        <div class="email-preview">Your order #123-4567890-1234567 has been shipped and will arrive by Friday...</div>
                        <span class="safe-badge">✓ SAFE</span>
                    </li>
                    
                    <li class="email-item phishing" onclick="showPhishingEmail('internal')">
                        <div class="email-time">8:22 AM</div>
                        <div class="email-sender">IT Department (itsupport@company.com)</div>
                        <div class="email-subject">URGENT: Mandatory Password Reset - Expires Today</div>
                        <div class="email-preview">Security vulnerabilities detected. All employees must reset passwords by 5 PM or accounts will be locked...</div>
                        <span class="warning-badge">⚠️ PHISHING</span>
                    </li>
                    
                    <li class="email-item phishing" onclick="showPhishingEmail('mpesa')">
                        <div class="email-time">Yesterday</div>
                        <div class="email-sender">Safaricom M-Pesa (noreply@safaricom-mpesa.com)</div>
                        <div class="email-subject">M-Pesa Account Verification Required - Action Needed</div>
                        <div class="email-preview">Verify your M-Pesa account by December 31st to avoid temporary suspension. Quick 2-minute process...</div>
                        <span class="warning-badge">⚠️ PHISHING</span>
                    </li>
                    
                    <li class="email-item safe" onclick="showSafeEmail()">
                        <div class="email-time">2 days ago</div>
                        <div class="email-sender">Google Security (no-reply@accounts.google.com)</div>
                        <div class="email-subject">Security alert - Suspicious sign-in prevented</div>
                        <div class="email-preview">We prevented a suspicious sign-in attempt to your Google Account. Review activity...</div>
                        <span class="safe-badge">✓ SAFE</span>
                    </li>
                </ul>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>91%</h3>
                    <p>Of cyberattacks start with phishing emails</p>
                </div>
                
                <div class="stat-card">
                    <h3>30%</h3>
                    <p>Average employee click rate on phishing emails</p>
                </div>
                
                <div class="stat-card">
                    <h3>$4.65M</h3>
                    <p>Average cost of a data breach in 2025</p>
                </div>
                
                <div class="stat-card">
                    <h3>82 days</h3>
                    <p>Average time to detect and contain a breach</p>
                </div>
            </div>
        </div>
        
        <!-- Phishing Modal -->
        <div id="phishingModal" class="modal">
            <div class="modal-content">
                <div class="modal-body" id="modalBody">
                    <!-- Content loaded dynamically -->
                </div>
            </div>
        </div>
        
        <script>
            let attackStage = 0;
            
            function showPhishingEmail(type) {
                attackStage = 1;
                const modal = document.getElementById('phishingModal');
                const body = document.getElementById('modalBody');
                
                if (type === 'banking') {
                    body.innerHTML = `
                        <div class="fake-bank-page">
                            <div class="url-bar">
                                <span class="lock">🔒</span>
                                <span class="fake-url">https://kcb-secure-verify.com/account/verify</span>
                            </div>
                            <div class="bank-header">
                                <div class="bank-logo">KCB BANK</div>
                            </div>
                            <div class="bank-alert">
                                ⚠️ URGENT SECURITY ALERT - IMMEDIATE ACTION REQUIRED
                            </div>
                            <div class="bank-form">
                                <h2 style="color: #333; margin-bottom: 20px; text-align: center;">Verify Your Identity</h2>
                                <p style="color: #666; margin-bottom: 25px; text-align: center;">
                                    Suspicious login attempts detected from Lagos, Nigeria.<br>
                                    Please verify your identity to keep your account secure.
                                </p>
                                
                                <div class="form-group">
                                    <label>Account Number / ID Number</label>
                                    <input type="text" placeholder="Enter your account or ID number" id="username">
                                </div>
                                
                                <div class="form-group">
                                    <label>PIN / Password</label>
                                    <input type="password" placeholder="Enter your PIN or password" id="password">
                                </div>
                                
                                <div class="form-group">
                                    <label>Phone Number</label>
                                    <input type="tel" placeholder="07XX XXX XXX" id="phone">
                                </div>
                                
                                <button class="btn btn-danger" onclick="captureCredentials('banking')">
                                    VERIFY MY ACCOUNT NOW
                                </button>
                                
                                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 20px;">
                                    ⏰ You have 23 hours remaining before automatic account suspension
                                </p>
                            </div>
                        </div>
                    `;
                } else if (type === 'mpesa') {
                    body.innerHTML = `
                        <div class="fake-bank-page">
                            <div class="url-bar">
                                <span class="lock">🔒</span>
                                <span class="fake-url">https://safaricom-mpesa-verify.co.ke/account</span>
                            </div>
                            <div class="mpesa-header">
                                <div class="mpesa-logo">M-PESA</div>
                                <div class="mpesa-tagline">by Safaricom</div>
                            </div>
                            <div class="bank-form">
                                <h2 style="color: #333; margin-bottom: 20px;">Account Verification</h2>
                                <p style="color: #666; margin-bottom: 25px; line-height: 1.6;">
                                    As part of our ongoing security improvements, we need you to verify your M-Pesa account. 
                                    This quick process ensures your account remains active and secure.
                                </p>
                                
                                <div class="form-group">
                                    <label>Registered Phone Number</label>
                                    <input type="tel" placeholder="07XX XXX XXX" id="mpesa-phone">
                                </div>
                                
                                <div class="form-group">
                                    <label>M-Pesa PIN</label>
                                    <input type="password" placeholder="Enter your 4-digit PIN" maxlength="4" id="mpesa-pin">
                                </div>
                                
                                <div class="form-group">
                                    <label>ID Number</label>
                                    <input type="text" placeholder="Enter your ID number" id="mpesa-id">
                                </div>
                                
                                <button class="btn btn-success" onclick="captureCredentials('mpesa')">
                                    Verify My Account
                                </button>
                                
                                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 20px;">
                                    🔒 Secure verification powered by Safaricom
                                </p>
                            </div>
                        </div>
                    `;
                } else if (type === 'internal') {
                    body.innerHTML = `
                        <div class="fake-bank-page">
                            <div class="url-bar">
                                <span class="lock">🔒</span>
                                <span class="fake-url">https://corporate-portal-login.company.com/reset</span>
                            </div>
                            <div style="background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 30px; text-align: center;">
                                <h2 style="margin: 0; font-size: 24px;">🔒 IT Security Portal</h2>
                                <p style="margin: 10px 0 0 0; opacity: 0.9;">Password Reset Required</p>
                            </div>
                            <div class="bank-form">
                                <div style="background: #fff4ce; border-left: 4px solid #ffb900; padding: 15px; margin-bottom: 25px;">
                                    <p style="margin: 0; color: #323130; font-size: 14px;">
                                        <strong>⚠️ Security Update:</strong> All employees must reset passwords by 5:00 PM today.
                                    </p>
                                </div>
                                
                                <div class="form-group">
                                    <label>Current Username / Email</label>
                                    <input type="text" placeholder="username@company.com" id="it-username">
                                </div>
                                
                                <div class="form-group">
                                    <label>Current Password</label>
                                    <input type="password" placeholder="Enter current password" id="it-old-pass">
                                </div>
                                
                                <div class="form-group">
                                    <label>New Password</label>
                                    <input type="password" placeholder="Create new password" id="it-new-pass">
                                </div>
                                
                                <div class="form-group">
                                    <label>Confirm New Password</label>
                                    <input type="password" placeholder="Confirm new password" id="it-confirm-pass">
                                </div>
                                
                                <button class="btn btn-primary" onclick="captureCredentials('internal')">
                                    Reset Password Now
                                </button>
                                
                                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 20px;">
                                    IT Department | itsupport@company.com | Ext. 5000
                                </p>
                            </div>
                        </div>
                    `;
                }
                
                modal.classList.add('active');
            }
            
            function captureCredentials(type) {
                attackStage = 2;
                const body = document.getElementById('modalBody');
                
                // Show loading
                body.innerHTML = `
                    <div class="loading active">
                        <div class="loader"></div>
                        <p style="color: #666;">Verifying your information...</p>
                    </div>
                `;
                
                // Simulate delay
                setTimeout(() => {
                    showAttackResults(type);
                }, 2000);
            }
            
            function showAttackResults(type) {
                const body = document.getElementById('modalBody');
                
                body.innerHTML = `
                    <div style="padding: 30px;">
                        <h2 style="color: #d9534f; margin-bottom: 20px; text-align: center; font-size: 28px;">
                            💀 YOU'VE BEEN PHISHED!
                        </h2>
                        
                        <p style="text-align: center; color: #666; font-size: 16px; margin-bottom: 30px;">
                            In a real attack, your credentials and account would now be fully compromised.
                        </p>
                        
                        <div class="captured-data">
                            <h3>🚨 Data Captured by Attacker:</h3>
                            <div class="data-item"><strong>IP Address:</strong> 197.156.89.234 (Nairobi, Kenya)</div>
                            <div class="data-item"><strong>Timestamp:</strong> ${new Date().toLocaleString('en-KE', { dateStyle: 'full', timeStyle: 'long' })}</div>
                            <div class="data-item"><strong>Browser:</strong> ${getBrowserName()} ${getBrowserVersion()}</div>
                            <div class="data-item"><strong>Operating System:</strong> ${getOS()}</div>
                            <div class="data-item"><strong>Device Type:</strong> ${getDeviceType()}</div>
                            <div class="data-item"><strong>Screen Resolution:</strong> ${screen.width}×${screen.height}</div>
                            <div class="data-item"><strong>Language/Locale:</strong> ${navigator.language}</div>
                            <div class="data-item"><strong>Time Zone:</strong> ${Intl.DateTimeFormat().resolvedOptions().timeZone}</div>
                            <div class="data-item"><strong>Credentials Entered:</strong> YES ✓ (Username, Password, ${type === 'mpesa' ? 'PIN, ' : ''}Phone)</div>
                        </div>
                        
                        <div class="timeline">
                            <h3 style="color: #333; margin-bottom: 20px;">Attack Timeline - What Just Happened:</h3>
                            
                            <div class="timeline-item">
                                <h4>0:00 - Phishing Email Sent</h4>
                                <p>Attacker sent fake ${type === 'banking' ? 'KCB Bank' : type === 'mpesa' ? 'M-Pesa' : 'IT Department'} email with urgent security alert to create panic.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>0:10 - Email Opened</h4>
                                <p>You opened the email. Attacker's tracking pixel confirmed email delivery and your IP address.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>0:15 - Phishing Link Clicked</h4>
                                <p>You clicked "Verify Account" button. Your device fingerprint (browser, OS, location) was captured.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>0:20 - Fake Login Page Loaded</h4>
                                <p>Redirected to attacker's fake website that looks identical to real ${type === 'banking' ? 'bank' : type === 'mpesa' ? 'M-Pesa' : 'company portal'}.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>0:25 - Credentials Entered</h4>
                                <p>You entered username, password, ${type === 'mpesa' ? 'PIN, ' : ''}and phone number. All data sent to attacker's server.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>0:27 - Data Stolen</h4>
                                <p>Attacker now has complete access: login credentials, device info, location, and contact details.</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>WITHIN 5 MINUTES - Account Takeover</h4>
                                <p>Attacker logs into your REAL account using stolen credentials. ${type === 'banking' || type === 'mpesa' ? 'Transfers money to untraceable accounts.' : 'Accesses company systems, steals data.'}</p>
                            </div>
                            
                            <div class="timeline-item">
                                <h4>WITHIN 1 HOUR - Maximum Damage</h4>
                                <p>${
                                    type === 'banking' ? 'Bank account drained. Loans taken in your name. Credit cards maxed out.' :
                                    type === 'mpesa' ? 'M-Pesa balance stolen. SIM swap attack initiated. Mobile banking compromised.' :
                                    'Company data exfiltrated. Ransomware deployed. Entire network compromised.'
                                }</p>
                            </div>
                        </div>
                        
                        <div class="warning-box">
                            <h3>🚨 Red Flags You Missed:</h3>
                            <ul>
                                ${type === 'banking' ? `
                                    <li><strong>Fake Domain:</strong> "kcb-secure-verify.com" - Real KCB uses "kcbgroup.com"</li>
                                    <li><strong>Suspicious URL:</strong> Legitimate banks never ask you to "verify" via email links</li>
                                    <li><strong>Urgency Tactics:</strong> "23 hours or suspension" - designed to bypass your rational thinking</li>
                                    <li><strong>Generic Greeting:</strong> Real bank would address you by name</li>
                                    <li><strong>Asking for PIN:</strong> Banks NEVER ask for your PIN via any channel</li>
                                ` : type === 'mpesa' ? `
                                    <li><strong>Wrong Domain:</strong> Real Safaricom uses "safaricom.co.ke" not "safaricom-mpesa.co.ke"</li>
                                    <li><strong>Email Communication:</strong> M-Pesa verifies via SMS/USSD, not email</li>
                                    <li><strong>Asking for PIN:</strong> Safaricom NEVER asks for your M-Pesa PIN</li>
                                    <li><strong>Suspension Threat:</strong> Fear tactic to rush your decision</li>
                                    <li><strong>ID Number Request:</strong> They already have this information</li>
                                ` : `
                                    <li><strong>Unexpected Request:</strong> IT would announce password resets via official channels</li>
                                    <li><strong>Short Deadline:</strong> Same-day deadline creates panic</li>
                                    <li><strong>Asks for Old Password:</strong> Real password resets don't need your old password</li>
                                    <li><strong>Email Link:</strong> IT would direct you to known internal portal, not email link</li>
                                    <li><strong>Generic Sender:</strong> Missing personal IT staff signatures/contact</li>
                                `}
                            </ul>
                        </div>
                        
                        <div class="success-box">
                            <h3>✅ But This Was TRAINING - You're Safe!</h3>
                            <p style="margin-bottom: 15px;">
                                No actual credentials were captured or stored. This simulation showed you exactly what a real 
                                phishing attack looks like and what happens when you fall for it.
                            </p>
                            
                            <h4 style="margin-top: 20px; margin-bottom: 10px;">What You Should Do Instead:</h4>
                            <ul>
                                <li><strong>Verify the sender:</strong> Check email domain carefully (not just display name)</li>
                                <li><strong>Never click email links:</strong> Type website URL directly into browser</li>
                                <li><strong>Check the URL:</strong> Look for wrong spelling, extra words, suspicious domains</li>
                                <li><strong>Be suspicious of urgency:</strong> Legitimate companies give reasonable time</li>
                                <li><strong>Never share credentials:</strong> Banks/services never ask for passwords via email</li>
                                <li><strong>Use 2FA:</strong> Two-factor authentication prevents credential-only attacks</li>
                                <li><strong>Verify independently:</strong> Call company directly using known phone numbers</li>
                                <li><strong>Report suspicious emails:</strong> Forward to IT/security team immediately</li>
                            </ul>
                            
                            <div style="margin-top: 25px; padding: 20px; background: white; border-radius: 8px; border: 2px solid #28a745;">
                                <h4 style="color: #155724; margin-bottom: 10px;">💡 Remember:</h4>
                                <p style="color: #155724; margin: 0;">
                                    <strong>If you're unsure, it's safer to do nothing and verify through official channels.</strong>
                                    A real urgency will still be urgent tomorrow. A fake one will disappear.
                                </p>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <button class="btn btn-primary" onclick="closeModal()">Close & Return to Inbox</button>
                        </div>
                    </div>
                `;
            }
            
            function showSafeEmail() {
                const modal = document.getElementById('phishingModal');
                const body = document.getElementById('modalBody');
                
                body.innerHTML = `
                    <div style="padding: 40px;">
                        <h2 style="color: #28a745; margin-bottom: 20px; text-align: center; font-size: 28px;">
                            ✓ This is a Legitimate Email
                        </h2>
                        
                        <div class="success-box">
                            <h3>Good job! You identified a safe email.</h3>
                            <p style="margin: 15px 0;">
                                This email is from a legitimate source and can be trusted.
                            </p>
                            
                            <h4 style="margin-top: 20px; margin-bottom: 10px;">Why this email is safe:</h4>
                            <ul>
                                <li><strong>Verified Domain:</strong> Email domain matches the official company domain</li>
                                <li><strong>Expected Communication:</strong> You were expecting this email or it's normal activity</li>
                                <li><strong>No Urgency:</strong> No threats, deadlines, or pressure tactics</li>
                                <li><strong>No Credentials Requested:</strong> Doesn't ask for passwords, PINs, or sensitive info</li>
                                <li><strong>Professional:</strong> Proper grammar, formatting, and company branding</li>
                                <li><strong>Verifiable:</strong> You can confirm by checking your account directly</li>
                            </ul>
                            
                            <div style="margin-top: 25px; padding: 20px; background: white; border-radius: 8px; border: 2px solid #28a745;">
                                <h4 style="color: #155724; margin-bottom: 10px;">Always Verify:</h4>
                                <p style="color: #155724; margin: 0;">
                                    Even safe-looking emails can be fakes. When in doubt, go directly to the 
                                    website (type URL yourself) instead of clicking email links.
                                </p>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <button class="btn btn-primary" onclick="closeModal()">Back to Inbox</button>
                        </div>
                    </div>
                `;
                
                modal.classList.add('active');
            }
            
            function closeModal() {
                attackStage = 0;
                document.getElementById('phishingModal').classList.remove('active');
            }
            
            function getBrowserName() {
                const agent = navigator.userAgent;
                if (agent.indexOf("Edg") > -1) return "Microsoft Edge";
                if (agent.indexOf("Chrome") > -1) return "Google Chrome";
                if (agent.indexOf("Firefox") > -1) return "Mozilla Firefox";
                if (agent.indexOf("Safari") > -1) return "Apple Safari";
                if (agent.indexOf("Opera") > -1) return "Opera";
                return "Unknown Browser";
            }
            
            function getBrowserVersion() {
                const agent = navigator.userAgent;
                const match = agent.match(/(Chrome|Firefox|Safari|Edge|Opera)\/([0-9.]+)/);
                return match ? match[2].split('.')[0] : '';
            }
            
            function getOS() {
                const agent = navigator.userAgent;
                if (agent.indexOf("Win") > -1) return "Windows " + (agent.indexOf("Windows NT 10.0") > -1 ? "10/11" : "");
                if (agent.indexOf("Mac") > -1) return "macOS";
                if (agent.indexOf("Linux") > -1) return "Linux";
                if (agent.indexOf("Android") > -1) return "Android";
                if (agent.indexOf("iOS") > -1 || agent.indexOf("iPhone") > -1) return "iOS";
                return "Unknown OS";
            }
            
            function getDeviceType() {
                const width = window.innerWidth;
                if (width < 768) return "Mobile Device";
                if (width < 1024) return "Tablet Device";
                return "Desktop Computer";
            }
            
            // Close modal on outside click or Escape key
            document.getElementById('phishingModal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal();
                }
            });
            
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        </script>
    </body>
    </html>
    """
    
    return html


