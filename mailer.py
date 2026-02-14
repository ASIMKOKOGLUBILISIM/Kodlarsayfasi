import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "KENDİ E-MAİLİNİZ"
APP_PASSWORD = "KENDİ UYGULAMA ŞİFRENİZ" 
RECEIVER_EMAIL = "KENDİ E-MAİLİNİZ"

def send_alert_mail(alert_type, severity, ip_address, country, attempt_count):
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Security Monitor <{SENDER_EMAIL}>"
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"🚨 {severity}: {alert_type} Detected from {country}"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Şiddete göre renk belirleme
    color = "#d9534f" if severity == "CRITICAL" else "#f0ad4e"

    # HTML İçeriği
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
            <div style="background-color: {color}; color: white; padding: 20px; text-align: center;">
                <h2 style="margin: 0;">SECURITY ALERT</h2>
            </div>
            <div style="padding: 20px;">
                <p><strong>Alert Type:</strong> {alert_type}</p>
                <p><strong>Severity:</strong> <span style="color: {color}; font-weight: bold;">{severity}</span></p>
                <p><strong>Detected At:</strong> {now}</p>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <h3>Saldırı Detayları</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 5px; font-weight: bold;">Source IP:</td><td>{ip_address}</td></tr>
                    <tr><td style="padding: 5px; font-weight: bold;">Location:</td><td>{country}</td></tr>
                    <tr><td style="padding: 5px; font-weight: bold;">Attempts:</td><td>{attempt_count} Failed Logins</td></tr>
                </table>
                <div style="margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-left: 5px solid {color};">
                    <strong>Recommended Action:</strong><br>
                    IP address has been automatically blocked. Please review logs for further investigation.
                </div>
            </div>
            <div style="background-color: #eee; padding: 10px; text-align: center; font-size: 12px; color: #777;">
                This is an automated message from your Security Monitoring Platform.
            </div>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"📧 HTML Alert mail gönderildi ({country})")
    except Exception as e:
        print("❌ Mail gönderim hatası:", e)