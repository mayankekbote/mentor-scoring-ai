import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.config import settings

def send_email(email_to: str, subject: str, html_content: str):
    if not settings.EMAILS_ENABLED:
        print(f"EMAILS_DISABLED: Would have sent email to {email_to} with subject: {subject}")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message["To"] = email_to

    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_PASSWORD:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM_EMAIL, email_to, message.as_string())
        print(f"Email sent successfully to {email_to}")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_reset_password_email(email_to: str, token: str):
    subject = "Password Reset Request - MentoraAI"
    reset_link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background-color:#f1f4f5;font-family:'Inter',Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f4f5;padding:48px 16px;">
            <tr>
                <td align="center">
                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;">

                        <!-- Header -->
                        <tr>
                            <td style="background-color:#0d9488;border-radius:16px 16px 0 0;padding:32px 40px;text-align:center;">
                                <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                                    <tr>
                                        <td style="background-color:rgba(255,255,255,0.15);border-radius:10px;padding:6px 14px;">
                                            <span style="color:#ffffff;font-size:20px;font-weight:800;letter-spacing:-0.03em;">Mentora<span style="opacity:0.75;">AI</span></span>
                                        </td>
                                    </tr>
                                </table>
                                <p style="color:rgba(255,255,255,0.7);font-size:13px;margin:12px 0 0;letter-spacing:0.02em;">Interview Intelligence Platform</p>
                            </td>
                        </tr>

                        <!-- Body -->
                        <tr>
                            <td style="background-color:#ffffff;padding:40px 40px 32px;">

                                <!-- Icon -->
                                <div style="text-align:center;margin-bottom:28px;">
                                    <div style="display:inline-block;background-color:#f0fdfa;border:1.5px solid #99f6e4;border-radius:50%;width:56px;height:56px;line-height:56px;text-align:center;font-size:24px;">🔑</div>
                                </div>

                                <h2 style="color:#0f172a;font-size:22px;font-weight:700;margin:0 0 12px;text-align:center;letter-spacing:-0.02em;">Reset your password</h2>
                                <p style="color:#64748b;font-size:15px;line-height:1.7;margin:0 0 28px;text-align:center;">
                                    We received a request to reset your password.<br/>Click the button below to choose a new one.
                                </p>

                                <!-- CTA -->
                                <div style="text-align:center;margin-bottom:28px;">
                                    <a href="{reset_link}"
                                       style="display:inline-block;background-color:#0d9488;color:#ffffff;font-size:15px;font-weight:600;padding:14px 36px;border-radius:10px;text-decoration:none;letter-spacing:-0.01em;">
                                        Reset Password →
                                    </a>
                                </div>

                                <!-- Expiry badge -->
                                <div style="text-align:center;margin-bottom:32px;">
                                    <span style="display:inline-block;background-color:#fef9c3;color:#854d0e;font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;border:1px solid #fde68a;">
                                        ⏱ Link expires in 30 minutes
                                    </span>
                                </div>

                                <!-- Divider -->
                                <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 0 24px;" />

                                <!-- Fallback link -->
                                <p style="color:#94a3b8;font-size:12px;line-height:1.6;margin:0;text-align:center;">
                                    If the button doesn't work, copy and paste this link:<br/>
                                    <a href="{reset_link}" style="color:#0d9488;word-break:break-all;font-size:11px;">{reset_link}</a>
                                </p>

                            </td>
                        </tr>

                        <!-- Ignore note -->
                        <tr>
                            <td style="background-color:#f8fafc;padding:20px 40px;border-top:1px solid #e2e8f0;">
                                <p style="color:#94a3b8;font-size:12px;line-height:1.6;margin:0;text-align:center;">
                                    Didn't request this? You can safely ignore this email — your password won't change.
                                </p>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background-color:#f1f4f5;border-radius:0 0 16px 16px;padding:20px 40px;text-align:center;">
                                <p style="color:#94a3b8;font-size:11px;margin:0;">© 2026 MentoraAI. All rights reserved.</p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    send_email(email_to, subject, html_content)

def send_interview_invitation_email(
    email_to: str, 
    candidate_name: str, 
    topic: str, 
    interview_date: str, 
    interview_time: str, 
    organization_name: str, 
    ai_score: int
):
    subject = "Interview Invitation - " + organization_name
    
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background-color:#f1f4f5;font-family:'Inter',Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f4f5;padding:48px 16px;">
            <tr>
                <td align="center">
                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color:#0d9488;border-radius:16px 16px 0 0;padding:32px 40px;text-align:center;">
                                <span style="color:#ffffff;font-size:24px;font-weight:800;letter-spacing:-0.03em;">Interview Invitation</span>
                            </td>
                        </tr>

                        <!-- Body -->
                        <tr>
                            <td style="background-color:#ffffff;padding:40px 40px 32px;border-radius:0 0 16px 16px;">
                                <h2 style="color:#0f172a;font-size:20px;font-weight:700;margin:0 0 16px;">Dear {candidate_name},</h2>
                                <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 24px;">
                                    Thank you for your teaching demonstration on <strong>"{topic}"</strong>. 
                                    Based on our evaluation, we are pleased to invite you to the next stage of our selection process.
                                </p>

                                <!-- Details Card -->
                                <div style="background-color:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;margin-bottom:24px;">
                                    <h3 style="color:#0f172a;font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;margin:0 0 16px;">Interview Details</h3>
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td style="color:#64748b;font-size:14px;padding-bottom:12px;">Date:</td>
                                            <td style="color:#0f172a;font-size:14px;font-weight:700;padding-bottom:12px;text-align:right;">{interview_date}</td>
                                        </tr>
                                        <tr>
                                            <td style="color:#64748b;font-size:14px;padding-bottom:12px;">Time:</td>
                                            <td style="color:#0f172a;font-size:14px;font-weight:700;padding-bottom:12px;text-align:right;">{interview_time}</td>
                                        </tr>
                                        <tr>
                                            <td style="color:#64748b;font-size:14px;padding-bottom:12px;">Organization:</td>
                                            <td style="color:#0f172a;font-size:14px;font-weight:700;padding-bottom:12px;text-align:right;">{organization_name}</td>
                                        </tr>
                                        <tr>
                                            <td style="color:#64748b;font-size:14px;">AI Evaluation Score:</td>
                                            <td style="color:#0d9488;font-size:15px;font-weight:800;text-align:right;">{ai_score}/100</td>
                                        </tr>
                                    </table>
                                </div>

                                <p style="color:#475569;font-size:14px;line-height:1.6;margin:0 0 24px;">
                                    Please confirm your availability by replying to this email. We look forward to meeting you!
                                </p>

                                <div style="border-top:1px solid #e2e8f0;padding-top:24px;margin-top:24px;">
                                    <p style="color:#64748b;font-size:13px;margin:0;">Best regards,</p>
                                    <p style="color:#0f172a;font-size:14px;font-weight:700;margin:4px 0 0;">HR Team</p>
                                    <p style="color:#64748b;font-size:13px;margin:2px 0 0;">{organization_name}</p>
                                </div>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="padding:24px 40px;text-align:center;">
                                <p style="color:#94a3b8;font-size:11px;margin:0;">© 2026 MentoraAI. Sent on behalf of {organization_name}.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    send_email(email_to, subject, html_content)