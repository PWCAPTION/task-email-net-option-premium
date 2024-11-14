import pandas as pd
from caption_ft_options_api.api_wrapper import FTOptionsAPI

from settings import RETURN_FIELDS


def get_security_df_from_ft_options_api(api: FTOptionsAPI) -> pd.DataFrame:
    df = api.get_position_risk_by_security(
        # account=Accounts.P2,
        return_fields=RETURN_FIELDS,
        dataframe=True,
    )
    return df


def get_ft_options_underliers(df_ft_options_api: pd.DataFrame) -> pd.Series:
    return df_ft_options_api["Underlyer"]


def remove_equity_securities(df: pd.DataFrame, accounts: list) -> pd.DataFrame:
    """This function removes equity type securities so only options remain. You can specify which accounts"""
    return df.loc[(df["Symbol"].str.len() > 10) & (df["Quantity"] != 0) & df["Account"].isin(accounts)]


def combine_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2], ignore_index=True)
