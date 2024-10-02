from django.core.mail import send_mail
from django.template.loader import render_to_string

from CareerCloset import settings

"""
Sends an email to the specified email address using the regular email template.
"""
def send_generic_email(to, subject, body):
    html_template = "generic-email.html"
    html_message = render_to_string(html_template, {'subject': subject, 'body': body, 'website_url': settings.WEBSITE_URL, 'reply_to_email': settings.REPLY_TO_EMAIL})
    send_mail(
        subject,
        '',
        settings.EMAIL_FROM,
        [to],
        html_message=html_message
    )