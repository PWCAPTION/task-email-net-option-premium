import os
from datetime import datetime

from caption_emailing import Emailer
from caption_emailing.caption_accounts import DEV


def send_email(subject: str, body: str, email_recipients: list[str]) -> None:
    emailer = Emailer.with_creds(username=DEV, password=os.getenv("DEV_EMAIL_PASS"))
    emailer.add_subject_to_email(subject)
    email_body = body
    emailer.add_body_to_email(email_body, subtype="HTML")
    emailer.email_account.send_email(
        email_recipients=email_recipients,
        email_object=emailer.email_obj,
    )


def generate_email_subject() -> str:
    return f"OptionPremium Report: {datetime.today().strftime('%-m/%-d/%y')}"


def generate_body_html(long_option_premium: int, short_option_premium: int, net_option_premium: int) -> str:
    body_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 20px;
        }}

        h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}

        p {{
            margin-bottom: 15px;
        }}

        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border: 1px solid #ccc;
        }}

        table {{
            border-collapse: collapse;
            margin-bottom: 20px;
            table-layout: auto;
        }}

        th {{
            background-color: #f2f2f2;
            text-align: center;
            padding: 8px;
            border: 1px solid #ddd;
            white-space: nowrap;
        }}

        td {{
            padding: 8px;
            border: 1px solid #ddd;
            white-space: nowrap;
        }}
    </style>
    <title>Results</title>
    </head>
    <body>

    <p>
    <b>Long OptionPremium: </b> {long_option_premium:,}
    </p>
    

    <p>
    <b>Short OptionPremium: </b> {short_option_premium:,}
    </p>

    <p>
    <b>Net OptionPremium: </b> {net_option_premium:,}
    </p>

    </body>
    </html>
    """
    return body_html
