from caption_emailing import caption_accounts
from caption_emailing.wrapper import email_on_failure
from caption_ft_options_api.api_wrapper import FTOptionsAPI

from settings import TASK_NAME
from utils.email import generate_body_html, generate_email_subject, send_email
from utils.ft_options import get_security_df_from_ft_options_api, remove_all_equities_from_positions_df
from utils.utils_func import calc_option_premium


@email_on_failure(TASK_NAME)
def main():
    df = get_security_df_from_ft_options_api(api=FTOptionsAPI.from_env())
    df = remove_all_equities_from_positions_df(df)
    df["Mark"] = df["Mark"].fillna(value=0)
    df = calc_option_premium(df)
    short_df = df[df["Quantity"] < 0]
    short_option_premium = short_df["OptionPremium"].sum()

    long_df = df[df["Quantity"] > 0]
    long_option_premium = long_df["OptionPremium"].sum()

    net_option_premium = df["OptionPremium"].sum()

    print(long_option_premium)
    print(short_option_premium)
    print(net_option_premium)

    # Send email with the above results to Trade Ops email plus Jeff G and Billy R
    subject = generate_email_subject()
    body_html = generate_body_html(long_option_premium, short_option_premium, net_option_premium)

    send_email(
        subject,
        body_html,
        [
            # caption_accounts.TRADEOPS,
            # caption_accounts.JEFFG,
            # caption_accounts.BILLY,
            caption_accounts.BRAYDEN,
            # caption_accounts.DAN,
            # caption_accounts.JASON,
            # caption_accounts.JAZMIN,
        ],
    )
    print("Net OptionPremium email sent")


if __name__ == "__main__":
    main()
