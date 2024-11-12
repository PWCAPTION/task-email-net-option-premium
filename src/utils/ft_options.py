import pandas as pd
from caption_ft_options_api.api_wrapper import FTOptionsAPI

from settings import RETURN_FIELDS

# from caption_ft_options_api.models.accounts import Accounts


def get_security_df_from_ft_options_api(api: FTOptionsAPI) -> pd.DataFrame:
    df = api.get_position_risk_by_security(
        # account=Accounts.P2,
        return_fields=RETURN_FIELDS,
        dataframe=True,
    )
    return df


def get_ft_options_underliers(df_ft_options_api: pd.DataFrame) -> pd.Series:
    return df_ft_options_api["Underlyer"]


def get_tickers_with_long_stock(df: pd.DataFrame, accounts: list) -> pd.DataFrame:
    """This function looks for any ticker that has a long stock position in any account and adds them to a dataframe series. You can specify which accounts"""
    return df.loc[(df["Symbol"].str.len() < 10) & (df["Quantity"] > 0) & df["Account"].isin(accounts)]


def sum_long_stock_by_symbol(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Symbol")["Quantity"].sum().reset_index()


def combine_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2], ignore_index=True)
