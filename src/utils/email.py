import os
from datetime import datetime

import pandas as pd
from caption_emailing import Emailer, caption_accounts
from caption_emailing.caption_accounts import DEV


def send_email(subject: str, body: str) -> None:
    emailer = Emailer.with_creds(username=DEV, password=os.getenv("DEV_EMAIL_PASS"))
    emailer.add_subject_to_email(subject)
    email_body = body
    emailer.add_body_to_email(email_body, subtype="HTML")
    emailer.email_account.send_email(
        email_recipients=[
            caption_accounts.TRADEOPS,
            caption_accounts.JEFFG,
            caption_accounts.BILLY,
            caption_accounts.BRAYDEN,
            caption_accounts.DAN,
            caption_accounts.JASON,
            # caption_accounts.JAZMIN,
        ],
        # email_recipients=[caption_accounts.BRAYDEN],
        email_object=emailer.email_obj,
    )


def generate_email_subject() -> str:
    return f"Long Stock Hard To Borrow Results {datetime.today().strftime('%-m/%-d/%y')}"


def generate_body_html(
    tickers_long_stock: pd.DataFrame,
    tickers_no_borrow_rate: pd.DataFrame,
) -> str:
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
    <h1>Results:</h1>

    <p>
    <b>P2 Tickers with long stock:</b>
        <code>{tickers_long_stock.to_html(index=False, classes='table table-striped')}</code>
        *Descending absolute value sort with negatives prioritized
    </p>
    

    <p>
    <b>P2 Tickers with long stock but WF gave no borrow rate:</b>
        <code>{tickers_no_borrow_rate.to_html(index=False, classes='table table-striped')}</code>
        *Probably due to these mostly being warrants
    </p>
    </body>
    </html>
    """
    return body_html