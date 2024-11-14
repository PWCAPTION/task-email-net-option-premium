from datetime import datetime, timedelta

import pandas as pd


def get_date(days: int) -> str:
    yesterday = datetime.now() - timedelta(days=days)

    # Format the date as YYYYMMDD
    return yesterday.strftime("%Y%m%d")


def clean_mark_column(df: pd.DataFrame) -> pd.DataFrame:
    """this function will remove rows if the mark column is not a number"""
    return df[pd.to_numeric(df["Mark"], errors="coerce").notna()]


def calc_option_premium(df: pd.DataFrame) -> pd.DataFrame:

    df["Option Premium"] = df["Quantity"] * df["Mark"] * 100
    df["Option Premium"] = df["Option Premium"].round().astype(int)
    df_calc = df
    return df_calc


def sum_option_premium(df: pd.DataFrame) -> pd.DataFrame:
    return int(df["Option Premium"].apply(lambda x: x if isinstance(x, int) else 0).sum())


def sum_short_option_premium(df: pd.DataFrame) -> pd.DataFrame:
    return int(df["Option Premium"].apply(lambda x: x if isinstance(x, int) and x < 0 else 0).sum())


def sum_long_option_premium(df: pd.DataFrame) -> pd.DataFrame:
    return int(df["Option Premium"].apply(lambda x: x if isinstance(x, int) and x > 0 else 0).sum())
