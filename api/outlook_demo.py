"""
Realistic Outlook + SMEAgent Demo
Shows authentic Microsoft Outlook interface with real-time threat detection
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/outlook-demo", response_class=HTMLResponse)
async def outlook_demo():
    """Pixel-perfect Microsoft Outlook demo with SMEAgent protection"""
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inbox - Outlook</title>
        <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
                background: #faf9f8;
                overflow: hidden;
                height: 100vh;
            }
            
            /* Top Bar */
            .top-bar {
                background: #0078d4;
                height: 48px;
                display: flex;
                align-items: center;
                padding: 0 16px;
                color: white;
            }
            
            .waffle-menu {
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                border-radius: 2px;
                font-size: 20px;
            }
            
            .waffle-menu:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            .outlook-title {
                margin-left: 16px;
                font-size: 15px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .search-box {
                flex: 1;
                max-width: 600px;
                margin-left: 40px;
                height: 32px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 2px;
                display: flex;
                align-items: center;
                padding: 0 12px;
            }
            
            .search-box input {
                border: none;
                background: transparent;
                flex: 1;
                outline: none;
                color: #323130;
                font-size: 14px;
            }
            
            .search-box input::placeholder {
                color: #605e5c;
            }
            
            .top-actions {
                margin-left: auto;
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            .top-btn {
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                border-radius: 2px;
                color: white;
            }
            
            .top-btn:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            /* Main Content Layout */
            .outlook-container {
                display: flex;
                height: calc(100vh - 48px);
            }
            
            /* Left Sidebar */
            .left-sidebar {
                width: 260px;
                background: #f3f2f1;
                border-right: 1px solid #edebe9;
                display: flex;
                flex-direction: column;
            }
            
            .sidebar-header {
                padding: 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .sidebar-title {
                font-size: 20px;
                font-weight: 600;
                color: #323130;
            }
            
            .new-email-btn {
                padding: 8px 24px;
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 2px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                margin: 0 16px 16px;
            }
            
            .new-email-btn:hover {
                background: #106ebe;
            }
            
            .folder-list {
                flex: 1;
                overflow-y: auto;
            }
            
            .folder-group {
                margin-bottom: 16px;
            }
            
            .folder-group-title {
                padding: 8px 16px;
                font-size: 11px;
                font-weight: 600;
                color: #605e5c;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .folder-item {
                padding: 8px 16px 8px 40px;
                display: flex;
                align-items: center;
                cursor: pointer;
                color: #323130;
                font-size: 14px;
                position: relative;
            }
            
            .folder-item:hover {
                background: #e1dfdd;
            }
            
            .folder-item.active {
                background: #edebe9;
                border-left: 3px solid #0078d4;
                font-weight: 600;
            }
            
            .folder-icon {
                position: absolute;
                left: 16px;
                font-size: 16px;
            }
            
            .folder-count {
                margin-left: auto;
                color: #605e5c;
                font-size: 12px;
                font-weight: 600;
            }
            
            /* Middle - Email List */
            .email-list-panel {
                width: 400px;
                background: white;
                border-right: 1px solid #edebe9;
                display: flex;
                flex-direction: column;
            }
            
            .list-toolbar {
                padding: 16px;
                border-bottom: 1px solid #edebe9;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .toolbar-section {
                display: flex;
                gap: 4px;
            }
            
            .toolbar-btn {
                padding: 6px 12px;
                border: none;
                background: transparent;
                color: #323130;
                font-size: 13px;
                cursor: pointer;
                border-radius: 2px;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .toolbar-btn:hover {
                background: #f3f2f1;
            }
            
            .filter-tabs {
                padding: 0 16px;
                display: flex;
                gap: 8px;
                border-bottom: 1px solid #edebe9;
            }
            
            .filter-tab {
                padding: 12px 16px;
                font-size: 14px;
                color: #323130;
                cursor: pointer;
                border-bottom: 2px solid transparent;
            }
            
            .filter-tab.active {
                color: #0078d4;
                border-bottom-color: #0078d4;
                font-weight: 600;
            }
            
            .filter-tab:hover {
                background: #f3f2f1;
            }
            
            .email-list {
                flex: 1;
                overflow-y: auto;
            }
            
            .email-item {
                padding: 16px;
                border-bottom: 1px solid #edebe9;
                cursor: pointer;
                position: relative;
                transition: all 0.15s;
            }
            
            .email-item:hover {
                background: #faf9f8;
            }
            
            .email-item.selected {
                background: #e1f3ff;
                border-left: 3px solid #0078d4;
            }
            
            .email-item.unread {
                background: #faf9f8;
            }
            
            .email-item.unread .email-from,
            .email-item.unread .email-subject {
                font-weight: 600;
            }
            
            .email-item.unread::before {
                content: '';
                position: absolute;
                left: 6px;
                top: 50%;
                transform: translateY(-50%);
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #0078d4;
            }
            
            .email-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 6px;
            }
            
            .email-from {
                font-size: 14px;
                color: #323130;
            }
            
            .email-time {
                font-size: 12px;
                color: #605e5c;
            }
            
            .email-subject {
                font-size: 14px;
                color: #323130;
                margin-bottom: 4px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .email-preview {
                font-size: 13px;
                color: #605e5c;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* New Email Animation */
            @keyframes slideInEmail {
                from {
                    transform: translateY(-20px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            .email-item.new-arrival {
                animation: slideInEmail 0.4s ease-out;
                background: #fff4ce !important;
            }
            
            /* Right - Reading Pane */
            .reading-pane {
                flex: 1;
                background: white;
                display: flex;
                flex-direction: column;
                position: relative;
            }
            
            .reading-pane-header {
                padding: 24px 32px 16px;
                border-bottom: 1px solid #edebe9;
            }
            
            .reading-toolbar {
                display: flex;
                gap: 8px;
                margin-bottom: 16px;
            }
            
            .reading-subject {
                font-size: 20px;
                font-weight: 600;
                color: #323130;
                margin-bottom: 16px;
            }
            
            .sender-info {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .sender-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #0078d4;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
            }
            
            .sender-details {
                flex: 1;
            }
            
            .sender-name {
                font-size: 14px;
                font-weight: 600;
                color: #323130;
            }
            
            .sender-email {
                font-size: 12px;
                color: #605e5c;
            }
            
            .email-timestamp {
                font-size: 12px;
                color: #605e5c;
            }
            
            .reading-pane-body {
                flex: 1;
                overflow-y: auto;
                padding: 24px 32px;
            }
            
            .email-body {
                font-size: 14px;
                line-height: 1.6;
                color: #323130;
            }
            
            .email-body p {
                margin-bottom: 16px;
            }
            
            .email-body strong {
                font-weight: 600;
            }
            
            .email-link {
                color: #0078d4;
                text-decoration: none;
                font-weight: 600;
            }
            
            .email-link:hover {
                text-decoration: underline;
            }
            
            .email-button {
                display: inline-block;
                padding: 12px 32px;
                background: #d13438;
                color: white;
                text-decoration: none;
                border-radius: 2px;
                font-weight: 600;
                margin: 16px 0;
            }
            
            /* SMEAgent Widget */
            .smeagent-widget {
                position: fixed;
                bottom: 24px;
                right: 24px;
                width: 400px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 6px 32px rgba(0, 0, 0, 0.2);
                overflow: hidden;
                transform: translateY(600px);
                transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
                z-index: 1000;
            }
            
            .smeagent-widget.visible {
                transform: translateY(0);
            }
            
            .smeagent-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                color: white;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .smeagent-icon {
                font-size: 32px;
            }
            
            .smeagent-title h3 {
                font-size: 16px;
                margin-bottom: 4px;
            }
            
            .smeagent-title p {
                font-size: 12px;
                opacity: 0.95;
            }
            
            .smeagent-body {
                padding: 24px;
            }
            
            .threat-alert-box {
                background: #fef6f6;
                border: 2px solid #d13438;
                border-radius: 6px;
                padding: 16px;
                margin-bottom: 20px;
            }
            
            .threat-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 12px;
            }
            
            .threat-icon {
                font-size: 24px;
            }
            
            .threat-title {
                font-size: 16px;
                font-weight: 600;
                color: #d13438;
            }
            
            .threat-description {
                color: #605e5c;
                font-size: 14px;
                line-height: 1.5;
                margin-left: 34px;
            }
            
            .threat-score-section {
                margin: 20px 0;
            }
            
            .score-label {
                font-size: 12px;
                color: #605e5c;
                margin-bottom: 8px;
                font-weight: 600;
            }
            
            .score-bar-wrapper {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .score-bar-track {
                flex: 1;
                height: 8px;
                background: #edebe9;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .score-bar-fill {
                height: 100%;
                background: linear-gradient(to right, #d13438, #a4262c);
                width: 0%;
                transition: width 2s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .score-value {
                font-size: 16px;
                font-weight: 600;
                color: #d13438;
            }
            
            .threat-details-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin: 20px 0;
            }
            
            .threat-detail-card {
                background: #faf9f8;
                padding: 12px;
                border-radius: 4px;
            }
            
            .detail-label {
                font-size: 11px;
                color: #8a8886;
                text-transform: uppercase;
                margin-bottom: 6px;
                letter-spacing: 0.5px;
            }
            
            .detail-value {
                font-size: 14px;
                font-weight: 600;
                color: #323130;
            }
            
            .detail-value.critical {
                color: #d13438;
            }
            
            .smeagent-actions {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            
            .smeagent-btn {
                padding: 12px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .btn-primary-action {
                background: #d13438;
                color: white;
            }
            
            .btn-primary-action:hover {
                background: #a4262c;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(209, 52, 56, 0.3);
            }
            
            .btn-secondary-action {
                background: white;
                color: #323130;
                border: 1px solid #8a8886;
            }
            
            .btn-secondary-action:hover {
                background: #f3f2f1;
            }
            
            .btn-full-width {
                grid-column: 1 / -1;
                background: white;
                color: #0078d4;
                border: 1px solid #0078d4;
            }
            
            .btn-full-width:hover {
                background: #deecf9;
            }
            
            /* Scanning Overlay */
            .scanning-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(3px);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 999;
            }
            
            .scanning-overlay.active {
                display: flex;
            }
            
            .scanning-card {
                background: white;
                padding: 48px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            }
            
            .scanning-spinner {
                width: 64px;
                height: 64px;
                border: 4px solid #edebe9;
                border-top-color: #667eea;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin: 0 auto 24px;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .scanning-title {
                font-size: 18px;
                font-weight: 600;
                color: #323130;
                margin-bottom: 8px;
            }
            
            .scanning-status {
                font-size: 14px;
                color: #605e5c;
            }
            
            /* Blocked Overlay */
            .blocked-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(4px);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 1001;
            }
            
            .blocked-overlay.active {
                display: flex;
            }
            
            .blocked-card {
                background: white;
                padding: 48px;
                border-radius: 8px;
                max-width: 600px;
                box-shadow: 0 8px 48px rgba(0, 0, 0, 0.3);
                border: 3px solid #d13438;
            }
            
            .blocked-icon-large {
                font-size: 72px;
                margin-bottom: 24px;
                text-align: center;
            }
            
            .blocked-title {
                font-size: 28px;
                font-weight: 600;
                color: #d13438;
                text-align: center;
                margin-bottom: 14px;
            }
            
            .blocked-text {
                font-size: 16px;
                color: #605e5c;
                line-height: 1.6;
                text-align: center;
                margin-bottom: 32px;
            }
            
            .comparison-section {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 32px;
            }
            
            .comparison-box {
                padding: 24px;
                border-radius: 6px;
            }
            
            .comparison-box.without {
                background: #fef6f6;
                border: 2px solid #d13438;
            }
            
            .comparison-box.with {
                background: #f3faf7;
                border: 2px solid #107c10;
            }
            
            .comparison-box h4 {
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 16px;
            }
            
            .comparison-box.without h4 {
                color: #d13438;
            }
            
            .comparison-box.with h4 {
                color: #107c10;
            }
            
            .comparison-box ul {
                list-style: none;
                font-size: 13px;
                line-height: 2;
            }
            
            .comparison-box.without li::before {
                content: '✗ ';
                color: #d13438;
                font-weight: 600;
                margin-right: 8px;
            }
            
            .comparison-box.with li::before {
                content: '✓ ';
                color: #107c10;
                font-weight: 600;
                margin-right: 8px;
            }
            
            /* Start Screen */
            .start-screen {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 2000;
                transition: opacity 0.5s;
            }
            
            .start-screen.hidden {
                opacity: 0;
                pointer-events: none;
            }
            
            .start-card {
                text-align: center;
                color: white;
                max-width: 650px;
                padding: 60px;
            }
            
            .start-card h1 {
                font-size: 52px;
                margin-bottom: 20px;
            }
            
            .start-card p {
                font-size: 20px;
                line-height: 1.6;
                margin-bottom: 40px;
                opacity: 0.95;
            }
            
            .start-btn {
                padding: 18px 48px;
                background: white;
                color: #667eea;
                border: none;
                border-radius: 4px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
                transition: all 0.3s;
            }
            
            .start-btn:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
            }
            
            .notification-pulse {
                position: absolute;
                top: 8px;
                right: 8px;
                width: 12px;
                height: 12px;
                background: #d13438;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.2); opacity: 0.8; }
            }
        </style>
    </head>
    <body>
        <!-- Start Screen -->
        <div class="start-screen" id="startScreen">
            <div class="start-card">
                <h1>🛡️ SMEAgent Live Demo</h1>
                <p>Experience exactly how SMEAgent detects and blocks phishing attacks in real-time within Microsoft Outlook.</p>
                <button class="start-btn" onclick="startDemo()">Start Live Demo</button>
            </div>
        </div>
        
        <!-- Scanning Overlay -->
        <div class="scanning-overlay" id="scanningOverlay">
            <div class="scanning-card">
                <div class="scanning-spinner"></div>
                <div class="scanning-title">SMEAgent Scanning Email...</div>
                <div class="scanning-status" id="scanningStatus">Analyzing threat patterns</div>
            </div>
        </div>
        
        <!-- Blocked Overlay -->
        <div class="blocked-overlay" id="blockedOverlay">
            <div class="blocked-card">
                <div class="blocked-icon-large">🛡️</div>
                <div class="blocked-title">Threat Blocked Successfully</div>
                <div class="blocked-text">
                    This phishing email was automatically detected and quarantined before it could do any harm. Your account and data remain secure.
                </div>
                
                <div class="comparison-section">
                    <div class="comparison-box without">
                        <h4>❌ Without SMEAgent</h4>
                        <ul>
                            <li>Email looks legitimate</li>
                            <li>You click the link</li>
                            <li>Credentials stolen</li>
                            <li>Account compromised</li>
                            <li>$50,000+ average loss</li>
                        </ul>
                    </div>
                    
                    <div class="comparison-box with">
                        <h4>✅ With SMEAgent</h4>
                        <ul>
                            <li>Instant detection (0.3s)</li>
                            <li>Automatic quarantine</li>
                            <li>Zero user interaction</li>
                            <li>Company protected</li>
                            <li>$0 loss prevented</li>
                        </ul>
                    </div>
                </div>
                
                <button class="smeagent-btn btn-primary-action" style="width: 100%; padding: 16px;" onclick="resetDemo()">
                    Return to Outlook
                </button>
            </div>
        </div>
        
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="waffle-menu">⊞</div>
            <div class="outlook-title">
                <span>📧</span>
                <span>Outlook</span>
            </div>
            <div class="search-box">
                <span>🔍</span>
                <input type="text" placeholder="Search mail and people">
            </div>
            <div class="top-actions">
                <div class="top-btn">🔔</div>
                <div class="top-btn">⚙️</div>
                <div class="top-btn">❓</div>
                <div class="top-btn">👤</div>
            </div>
        </div>
        
        <!-- Main Outlook Container -->
        <div class="outlook-container">
            <!-- Left Sidebar -->
            <div class="left-sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-title">Folders</div>
                </div>
                <button class="new-email-btn">✉️ New mail</button>
                
                <div class="folder-list">
                    <div class="folder-group">
                        <div class="folder-group-title">Favorites</div>
                        <div class="folder-item active">
                            <span class="folder-icon">📥</span>
                            Inbox
                            <span class="folder-count" id="inboxCount">7</span>
                        </div>
                    </div>
                    
                    <div class="folder-group">
                        <div class="folder-group-title">Folders</div>
                        <div class="folder-item">
                            <span class="folder-icon">📤</span>
                            Sent Items
                        </div>
                        <div class="folder-item">
                            <span class="folder-icon">📝</span>
                            Drafts
                            <span class="folder-count">2</span>
                        </div>
                        <div class="folder-item">
                            <span class="folder-icon">🗑️</span>
                            Deleted Items
                        </div>
                        <div class="folder-item">
                            <span class="folder-icon">📁</span>
                            Archive
                        </div>
                        <div class="folder-item">
                            <span class="folder-icon">⚠️</span>
                            Junk Email
                        </div>
                        <div class="folder-item">
                            <span class="folder-icon">🛡️</span>
                            SMEAgent Quarantine
                            <span class="folder-count" id="quarantineCount">0</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Email List Panel -->
            <div class="email-list-panel">
                <div class="list-toolbar">
                    <div class="toolbar-section">
                        <button class="toolbar-btn">☑️ Select all</button>
                    </div>
                    <div class="toolbar-section" style="margin-left: auto;">
                        <button class="toolbar-btn">⬅️</button>
                        <button class="toolbar-btn">➡️</button>
                    </div>
                </div>
                
                <div class="filter-tabs">
                    <div class="filter-tab active">Focused</div>
                    <div class="filter-tab">Other</div>
                </div>
                
                <div class="email-list" id="emailList">
                    <!-- Phishing Emails (will trigger scan) -->
                    <div class="email-item unread" data-phishing="true" data-email-id="phishing1">
                        <div class="email-header">
                            <div class="email-from">KCB Bank Security</div>
                            <div class="email-time">11:45 AM</div>
                        </div>
                        <div class="email-subject">🔒 URGENT: Suspicious Activity on Your Account</div>
                        <div class="email-preview">We detected unusual login attempts from Lagos, Nigeria. Verify immediately to prevent account suspension...</div>
                    </div>
                    
                    <!-- Legitimate Emails -->
                    <div class="email-item unread" data-email-id="legit1">
                        <div class="email-header">
                            <div class="email-from">Sarah Wanjiku</div>
                            <div class="email-time">11:30 AM</div>
                        </div>
                        <div class="email-subject">Re: Q4 Budget Review Meeting</div>
                        <div class="email-preview">Thanks for scheduling. I've reviewed the numbers and have some suggestions for the presentation...</div>
                    </div>
                    
                    <div class="email-item" data-phishing="true" data-email-id="phishing2">
                        <div class="email-header">
                            <div class="email-from">M-Pesa Customer Care</div>
                            <div class="email-time">10:22 AM</div>
                        </div>
                        <div class="email-subject">⚠️ Your M-Pesa Account Will Be Closed</div>
                        <div class="email-preview">Action required: Update your details within 24 hours or lose access to your KSh 45,230 balance...</div>
                    </div>
                    
                    <div class="email-item" data-email-id="legit2">
                        <div class="email-header">
                            <div class="email-from">LinkedIn</div>
                            <div class="email-time">10:15 AM</div>
                        </div>
                        <div class="email-subject">You appeared in 15 searches this week</div>
                        <div class="email-preview">See who's been looking at your profile. Upgrade to premium to view all profile visitors...</div>
                    </div>
                    
                    <div class="email-item" data-email-id="legit3">
                        <div class="email-header">
                            <div class="email-from">Amazon.com</div>
                            <div class="email-time">Yesterday</div>
                        </div>
                        <div class="email-subject">Your order has shipped</div>
                        <div class="email-preview">Good news! Your package is on its way. Track your shipment to see delivery details...</div>
                    </div>
                    
                    <div class="email-item" data-phishing="true" data-email-id="phishing3">
                        <div class="email-header">
                            <div class="email-from">IT Department</div>
                            <div class="email-time">Yesterday</div>
                        </div>
                        <div class="email-subject">URGENT: Email Password Expiring Today</div>
                        <div class="email-preview">Your email password expires in 2 hours. Click here to reset and avoid losing access to your mailbox...</div>
                    </div>
                    
                    <div class="email-item" data-email-id="legit4">
                        <div class="email-header">
                            <div class="email-from">David Ochieng</div>
                            <div class="email-time">2 days ago</div>
                        </div>
                        <div class="email-subject">Client presentation materials</div>
                        <div class="email-preview">Attached are the updated slides for next week's client presentation. Let me know if you need anything else...</div>
                    </div>
                </div>
            </div>
            
            <!-- Reading Pane -->
            <div class="reading-pane">
                <div class="reading-pane-header">
                    <div class="reading-toolbar">
                        <button class="toolbar-btn">↩️ Reply</button>
                        <button class="toolbar-btn">⤴️ Forward</button>
                        <button class="toolbar-btn">🗑️ Delete</button>
                    </div>
                    
                    <div class="reading-subject">Re: Q4 Budget Review Meeting</div>
                    
                    <div class="sender-info">
                        <div class="sender-avatar">SW</div>
                        <div class="sender-details">
                            <div class="sender-name">Sarah Wanjiku</div>
                            <div class="sender-email">sarah.wanjiku@company.co.ke</div>
                        </div>
                        <div class="email-timestamp">Today, 11:30 AM</div>
                    </div>
                </div>
                
                <div class="reading-pane-body">
                    <div class="email-body">
                        <p>Hi John,</p>
                        <p>Thanks for scheduling the Q4 budget review meeting. I've gone through the preliminary numbers and have a few suggestions for our presentation to the board:</p>
                        <p><strong>Key Points:</strong></p>
                        <p>1. Marketing spend is up 15% but ROI improved by 23%<br>
                        2. Cloud infrastructure costs reduced by $12K/month<br>
                        3. New client acquisition exceeded targets by 18%</p>
                        <p>I'll prepare detailed slides for Thursday's meeting. Let me know if you need anything else.</p>
                        <p>Best regards,<br>
                        <strong>Sarah Wanjiku</strong><br>
                        Finance Manager<br>
                        Tel: +254 712 345 678</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- SMEAgent Widget -->
        <div class="smeagent-widget" id="smeagentWidget">
            <div class="smeagent-header">
                <div class="smeagent-icon">🛡️</div>
                <div class="smeagent-title">
                    <h3>SMEAgent Protection</h3>
                    <p>Real-time Email Security</p>
                </div>
            </div>
            
            <div class="smeagent-body">
                <div class="threat-alert-box">
                    <div class="threat-header">
                        <span class="threat-icon">⚠️</span>
                        <span class="threat-title">Phishing Attack Detected</span>
                    </div>
                    <div class="threat-description">
                        Suspicious email from <strong id="threatSender">KCB Bank Security</strong> was detected and automatically quarantined.
                    </div>
                </div>
                
                <div class="threat-score-section">
                    <div class="score-label">THREAT LEVEL</div>
                    <div class="score-bar-wrapper">
                        <div class="score-bar-track">
                            <div class="score-bar-fill" id="scoreBarFill"></div>
                        </div>
                        <div class="score-value">95/100</div>
                    </div>
                </div>
                
                <div class="threat-details-grid">
                    <div class="threat-detail-card">
                        <div class="detail-label">Threat Type</div>
                        <div class="detail-value">Credential Phishing</div>
                    </div>
                    <div class="threat-detail-card">
                        <div class="detail-label">Risk Level</div>
                        <div class="detail-value critical">CRITICAL</div>
                    </div>
                    <div class="threat-detail-card">
                        <div class="detail-label">Action Taken</div>
                        <div class="detail-value">Quarantined</div>
                    </div>
                    <div class="threat-detail-card">
                        <div class="detail-label">Detection Time</div>
                        <div class="detail-value">0.3 seconds</div>
                    </div>
                </div>
                
                <div class="smeagent-actions">
                    <button class="smeagent-btn btn-primary-action" onclick="blockThreat()">🛡️ Keep Blocked</button>
                    <button class="smeagent-btn btn-secondary-action" onclick="showWarning()">⚠️ Allow</button>
                    <button class="smeagent-btn btn-full-width" onclick="showDetails()">📊 View Full Analysis</button>
                </div>
            </div>
        </div>
        
        <script>
            let demoStarted = false;
            let currentEmail = null;
            let selectedEmailElement = null;
            
            // Email content data
            const emailContents = {
                phishing1: {
                    from: "KCB Bank Security",
                    email: "security@kcb-alerts.com",
                    subject: "🔒 URGENT: Suspicious Activity on Your Account",
                    time: "Today, 11:45 AM",
                    body: `
                        <p>Dear Valued Customer,</p>
                        <p><strong>IMMEDIATE ACTION REQUIRED</strong></p>
                        <p>We have detected <strong style="color: #d13438;">suspicious login attempts</strong> on your KCB Bank account from Lagos, Nigeria at 11:32 AM today.</p>
                        <p>For your security, we have temporarily limited access to your account. You must verify your identity immediately to prevent permanent suspension.</p>
                        <p><strong>Account Details:</strong><br>
                        Account Number: ****7892<br>
                        Last Login: Lagos, Nigeria<br>
                        Status: <span style="color: #d13438;">SUSPENDED</span></p>
                        <p style="margin: 20px 0;">
                            <a href="http://kcb-verify-account.com" class="email-button">VERIFY YOUR ACCOUNT NOW</a>
                        </p>
                        <p style="color: #d13438;"><strong>⚠️ You have 2 hours to verify or your account will be permanently closed.</strong></p>
                        <p>KCB Bank Security Team<br>
                        Email: security@kcb-alerts.com</p>
                    `,
                    isPhishing: true,
                    threatInfo: {
                        sender: "KCB Bank Security (fake)",
                        score: 95
                    }
                },
                phishing2: {
                    from: "M-Pesa Customer Care",
                    email: "support@mpesa-ke.com",
                    subject: "⚠️ Your M-Pesa Account Will Be Closed",
                    time: "Today, 10:22 AM",
                    body: `
                        <p>Hello,</p>
                        <p><strong>IMPORTANT NOTICE</strong></p>
                        <p>Due to new government regulations, all M-Pesa accounts must be updated with current KRA PIN details within 24 hours.</p>
                        <p><strong style="color: #d13438;">Your current balance: KSh 45,230.00</strong></p>
                        <p>Failure to update your details will result in:</p>
                        <p>❌ Account closure<br>
                        ❌ Loss of access to your balance<br>
                        ❌ Inability to receive or send money</p>
                        <p style="margin: 20px 0;">
                            <a href="http://mpesa-update.co.ke" class="email-button">UPDATE DETAILS NOW</a>
                        </p>
                        <p><strong>Deadline: </strong><span style="color: #d13438;">November 23, 2024 - 11:59 PM</span></p>
                        <p>M-Pesa Customer Service<br>
                        Safaricom PLC</p>
                    `,
                    isPhishing: true,
                    threatInfo: {
                        sender: "M-Pesa Customer Care (fake)",
                        score: 92
                    }
                },
                phishing3: {
                    from: "IT Department",
                    email: "it-support@company-mail.com",
                    subject: "URGENT: Email Password Expiring Today",
                    time: "Yesterday, 4:15 PM",
                    body: `
                        <p>Dear Employee,</p>
                        <p><strong>EMAIL PASSWORD EXPIRATION NOTICE</strong></p>
                        <p>Your company email password will expire in <strong style="color: #d13438;">2 hours</strong>. You must reset it immediately to maintain access to your mailbox.</p>
                        <p>If you do not reset your password, you will:</p>
                        <p>• Lose access to all emails<br>
                        • Be unable to receive critical business communications<br>
                        • Need to contact IT for a manual reset (3-5 business days)</p>
                        <p style="margin: 20px 0;">
                            <a href="http://company-password-reset.com" class="email-button">RESET PASSWORD NOW</a>
                        </p>
                        <p><strong>Time Remaining: </strong><span style="color: #d13438;">1 hour 47 minutes</span></p>
                        <p>IT Support Department<br>
                        Tel: +254 700 000 000<br>
                        Email: it-support@company-mail.com</p>
                    `,
                    isPhishing: true,
                    threatInfo: {
                        sender: "IT Department (spoofed)",
                        score: 88
                    }
                },
                legit1: {
                    from: "Sarah Wanjiku",
                    email: "sarah.wanjiku@company.co.ke",
                    subject: "Re: Q4 Budget Review Meeting",
                    time: "Today, 11:30 AM",
                    body: `
                        <p>Hi John,</p>
                        <p>Thanks for scheduling the Q4 budget review meeting. I've gone through the preliminary numbers and have a few suggestions for our presentation to the board:</p>
                        <p><strong>Key Points:</strong></p>
                        <p>1. Marketing spend is up 15% but ROI improved by 23%<br>
                        2. Cloud infrastructure costs reduced by $12K/month<br>
                        3. New client acquisition exceeded targets by 18%</p>
                        <p>I'll prepare detailed slides for Thursday's meeting. Let me know if you need anything else.</p>
                        <p>Best regards,<br>
                        <strong>Sarah Wanjiku</strong><br>
                        Finance Manager<br>
                        Tel: +254 712 345 678</p>
                    `,
                    isPhishing: false
                },
                legit2: {
                    from: "LinkedIn",
                    email: "messages-noreply@linkedin.com",
                    subject: "You appeared in 15 searches this week",
                    time: "Today, 10:15 AM",
                    body: `
                        <p>Hi there,</p>
                        <p>People are checking out your profile! You appeared in <strong>15 searches</strong> this week.</p>
                        <p><strong>Top viewers by industry:</strong><br>
                        • Technology & Software: 6 views<br>
                        • Financial Services: 4 views<br>
                        • Professional Services: 3 views</p>
                        <p>Upgrade to LinkedIn Premium to see who's been viewing your profile and expand your professional network.</p>
                        <p style="margin: 20px 0;">
                            <a href="#" class="email-link">See who viewed your profile</a>
                        </p>
                        <p>The LinkedIn Team</p>
                    `,
                    isPhishing: false
                },
                legit3: {
                    from: "Amazon.com",
                    email: "ship-confirm@amazon.com",
                    subject: "Your order has shipped",
                    time: "Yesterday",
                    body: `
                        <p>Hello,</p>
                        <p>Good news! Your package is on its way.</p>
                        <p><strong>Shipping Details:</strong><br>
                        Order #: 702-8394756-1847392<br>
                        Carrier: DHL Express<br>
                        Tracking #: 3847562910376<br>
                        Expected Delivery: November 24, 2024</p>
                        <p>Items in this shipment:<br>
                        • Logitech MX Master 3 Mouse - Qty: 1</p>
                        <p style="margin: 20px 0;">
                            <a href="#" class="email-link">Track your package</a>
                        </p>
                        <p>Thanks for shopping with us!<br>
                        Amazon.com</p>
                    `,
                    isPhishing: false
                },
                legit4: {
                    from: "David Ochieng",
                    email: "david.ochieng@company.co.ke",
                    subject: "Client presentation materials",
                    time: "2 days ago",
                    body: `
                        <p>Hi Team,</p>
                        <p>Attached are the updated slides for next week's client presentation.</p>
                        <p><strong>Changes made:</strong></p>
                        <p>• Updated revenue projections based on Q3 actuals<br>
                        • Added case studies from similar implementations<br>
                        • Revised timeline to be more conservative<br>
                        • Included competitor analysis</p>
                        <p>Please review and send any feedback by Friday. We'll do a full run-through on Monday morning.</p>
                        <p>Thanks,<br>
                        <strong>David Ochieng</strong><br>
                        Senior Account Manager<br>
                        Tel: +254 722 456 789</p>
                    `,
                    isPhishing: false
                }
            };
            
            function startDemo() {
                demoStarted = true;
                document.getElementById('startScreen').classList.add('hidden');
                
                // Add click handlers to all emails
                const emailItems = document.querySelectorAll('.email-item');
                emailItems.forEach(item => {
                    item.addEventListener('click', function() {
                        selectEmail(this);
                    });
                });
                
                // Select first email by default
                if (emailItems.length > 0) {
                    selectEmail(emailItems[1]); // Select Sarah's email (legitimate)
                }
            }
            
            function selectEmail(emailElement) {
                // Remove previous selection
                if (selectedEmailElement) {
                    selectedEmailElement.classList.remove('selected');
                }
                
                // Mark as selected
                emailElement.classList.add('selected');
                emailElement.classList.remove('unread');
                selectedEmailElement = emailElement;
                
                // Get email data
                const emailId = emailElement.getAttribute('data-email-id');
                const emailData = emailContents[emailId];
                const isPhishing = emailElement.getAttribute('data-phishing') === 'true';
                
                if (!emailData) return;
                
                currentEmail = emailData;
                
                // Update reading pane
                updateReadingPane(emailData);
                
                // If phishing email, trigger scan
                if (isPhishing) {
                    setTimeout(() => {
                        triggerScan(emailData);
                    }, 800);
                }
            }
            
            function updateReadingPane(emailData) {
                const readingPane = document.querySelector('.reading-pane');
                
                // Get sender initials
                const initials = emailData.from.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
                
                readingPane.innerHTML = `
                    <div class="reading-pane-header">
                        <div class="reading-toolbar">
                            <button class="toolbar-btn">↩️ Reply</button>
                            <button class="toolbar-btn">⤴️ Forward</button>
                            <button class="toolbar-btn">🗑️ Delete</button>
                        </div>
                        
                        <div class="reading-subject">${emailData.subject}</div>
                        
                        <div class="sender-info">
                            <div class="sender-avatar">${initials}</div>
                            <div class="sender-details">
                                <div class="sender-name">${emailData.from}</div>
                                <div class="sender-email">${emailData.email}</div>
                            </div>
                            <div class="email-timestamp">${emailData.time}</div>
                        </div>
                    </div>
                    
                    <div class="reading-pane-body">
                        <div class="email-body">
                            ${emailData.body}
                        </div>
                    </div>
                `;
            }
            
            function triggerScan(emailData) {
                const overlay = document.getElementById('scanningOverlay');
                const status = document.getElementById('scanningStatus');
                
                overlay.classList.add('active');
                
                const scanSteps = [
                    'Analyzing sender reputation...',
                    'Checking domain authenticity...',
                    'Scanning for malicious links...',
                    'Comparing against threat database...',
                    'Evaluating urgency tactics...',
                    'THREAT DETECTED!'
                ];
                
                let step = 0;
                const interval = setInterval(() => {
                    if (step < scanSteps.length) {
                        status.textContent = scanSteps[step];
                        step++;
                    } else {
                        clearInterval(interval);
                        completeScan(emailData);
                    }
                }, 600);
            }
            
            function completeScan(emailData) {
                const overlay = document.getElementById('scanningOverlay');
                const widget = document.getElementById('smeagentWidget');
                
                // Update widget with email-specific threat info
                document.getElementById('threatSender').textContent = emailData.threatInfo.sender;
                document.querySelector('.score-value').textContent = emailData.threatInfo.score + '/100';
                
                // Hide scanning overlay
                setTimeout(() => {
                    overlay.classList.remove('active');
                    
                    // Show SMEAgent widget
                    setTimeout(() => {
                        widget.classList.add('visible');
                        
                        // Animate threat score bar
                        setTimeout(() => {
                            document.getElementById('scoreBarFill').style.width = emailData.threatInfo.score + '%';
                        }, 300);
                        
                        // Quarantine the email
                        quarantineEmail();
                    }, 300);
                }, 500);
            }
            
            function quarantineEmail() {
                const emailList = document.getElementById('emailList');
                const inboxCount = document.getElementById('inboxCount');
                const quarantineCount = document.getElementById('quarantineCount');
                
                // Highlight selected email as quarantined after 2 seconds
                setTimeout(() => {
                    if (selectedEmailElement) {
                        selectedEmailElement.style.background = '#fef6f6';
                        selectedEmailElement.style.border = '2px solid #d13438';
                        
                        // Remove after another second
                        setTimeout(() => {
                            selectedEmailElement.style.transform = 'translateX(-100%)';
                            selectedEmailElement.style.opacity = '0';
                            selectedEmailElement.style.transition = 'all 0.3s';
                            
                            setTimeout(() => {
                                selectedEmailElement.remove();
                                const currentCount = parseInt(inboxCount.textContent);
                                inboxCount.textContent = (currentCount - 1).toString();
                                
                                const currentQuarantine = parseInt(quarantineCount.textContent || '0');
                                quarantineCount.textContent = (currentQuarantine + 1).toString();
                                
                                selectedEmailElement = null;
                            }, 300);
                        }, 1000);
                    }
                }, 2000);
            }
            
            function blockThreat() {
                const widget = document.getElementById('smeagentWidget');
                const blocked = document.getElementById('blockedOverlay');
                
                widget.classList.remove('visible');
                
                setTimeout(() => {
                    blocked.classList.add('active');
                }, 300);
            }
            
            function showWarning() {
                if (confirm('⚠️ WARNING: This email is highly likely to be a phishing attack.\\n\\nAllowing this email could result in:\\n• Stolen credentials\\n• Account compromise\\n• Financial loss\\n• Data breach\\n\\nAre you absolutely sure?')) {
                    alert('🛡️ SMEAgent: This action is not recommended. The email will remain in quarantine for your safety.');
                }
            }
            
            function showDetails() {
                const threatScore = currentEmail?.threatInfo?.score || 95;
                const threatSender = currentEmail?.threatInfo?.sender || 'Unknown sender';
                
                alert(
                    '📊 SMEAgent Threat Analysis\\n\\n' +
                    '🎯 Threat Type: Credential Phishing\\n' +
                    '🔴 Risk Level: CRITICAL (' + threatScore + '/100)\\n\\n' +
                    'Red Flags Detected:\\n' +
                    '✗ Sender domain mismatch\\n' +
                    '✗ Urgent language and time pressure tactics\\n' +
                    '✗ Malicious link to fake login page\\n' +
                    '✗ Sender reputation: -87/100 (known phishing)\\n' +
                    '✗ Email not from official mail servers\\n' +
                    '✗ Link destination: phishing site detected\\n\\n' +
                    '🛡️ Action: Quarantined automatically\\n' +
                    '⏱️ Detection time: 0.3 seconds\\n' +
                    '💰 Estimated loss prevented: $50,000+'
                );
            }
            
            function resetDemo() {
                location.reload();
            }
        </script>
    </body>
    </html>
    """
    
    return html
