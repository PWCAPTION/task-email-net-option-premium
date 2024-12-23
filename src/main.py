from caption_emailing import caption_accounts
from caption_emailing.wrapper import email_on_failure
from caption_ft_options_api.api_wrapper import FTOptionsAPI

from settings import TASK_NAME
from utils.email import generate_body_html, generate_email_subject, send_email
from utils.ft_options import get_security_df_from_ft_options_api, remove_all_equities_from_positions_df
from utils.utils_func import calc_option_premium

"""
simplify names to df
pull filtering out of functions
use aws utils for pulling files
"""


@email_on_failure(TASK_NAME)
def main():
    df = get_security_df_from_ft_options_api(api=FTOptionsAPI.from_env())
    # df2 = df.loc[(df["Symbol"].str.len() > 10) & (df["Quantity"] != 0) & df["Account"].isin(["P1", "P2", "CHEF", "PH", "NHC", "NHC2"])]
    df = remove_all_equities_from_positions_df(df)
    df["Mark"] = df["Mark"].fillna(value=0)
    df = calc_option_premium(df)

    # short_df = df[df["Quantity"] < 0]
    short_df = df[df["OptionPremium"] < 0]
    short_option_premium = short_df["OptionPremium"].sum().round().astype(int)
    short_option_premium = "{:,}".format(short_option_premium)

    # long_df = df[df["Quantity"] > 0]
    long_df = df[df["OptionPremium"] > 0]
    long_option_premium = long_df["OptionPremium"].sum().round().astype(int)
    long_option_premium = "{:,}".format(long_option_premium)

    net_option_premium = df["OptionPremium"].sum().round().astype(int)
    net_option_premium = "{:,}".format(net_option_premium)

    print(long_option_premium)
    print(short_option_premium)
    print(net_option_premium)

    subject = generate_email_subject()
    body_html = generate_body_html(long_option_premium, short_option_premium, net_option_premium)

    send_email(
        subject,
        body_html,
        [caption_accounts.TRADEOPS, caption_accounts.JEFFG, caption_accounts.BILLY, caption_accounts.BRAYDEN, caption_accounts.DAN, caption_accounts.JASON, "jramirez@captionpartners.com", "jknapp@captionpartners.com"],
    )
    print("Net OptionPremium email sent")


if __name__ == "__main__":
    main()
