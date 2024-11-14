from caption_emailing.wrapper import email_on_failure
from caption_ft_options_api.api_wrapper import FTOptionsAPI
from caption_logger.logger import get_logger

from settings import TASK_NAME
from utils.email import generate_body_html, generate_email_subject, send_email
from utils.ft_options import get_security_df_from_ft_options_api, remove_equity_securities
from utils.utils_func import calc_option_premium, clean_mark_column, sum_long_option_premium, sum_option_premium, sum_short_option_premium


@email_on_failure(TASK_NAME)
def main():

    logger = get_logger()
    logger.info(f"Starting {TASK_NAME}")

    df_ft_options_api = get_security_df_from_ft_options_api(api=FTOptionsAPI.from_env())
    df_ft_options_api_filtered = remove_equity_securities(df_ft_options_api, ["P1", "P2", "CHEF", "PH", "NHC", "NHC2"])
    df_ft_options_api_filtered_cleaned = clean_mark_column(df_ft_options_api_filtered)
    df_net_premium_calculated = calc_option_premium(df_ft_options_api_filtered_cleaned)
    long_option_premium = sum_long_option_premium(df_net_premium_calculated)
    short_option_premium = sum_short_option_premium(df_net_premium_calculated)
    net_option_premium = sum_option_premium(df_net_premium_calculated)

    print(long_option_premium)
    print(short_option_premium)
    print(net_option_premium)

    # Send email with the above results to Trade Ops email plus Jeff G and Billy R
    subject = generate_email_subject()
    body_html = generate_body_html(long_option_premium, short_option_premium, net_option_premium)

    send_email(subject, body_html)
    logger.info("Net Option Premium email sent")
    logger.info(f"Finished {TASK_NAME}")


if __name__ == "__main__":
    main()
