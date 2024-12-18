from datetime import datetime, timedelta

import pandas as pd


def get_date(days: int) -> str:
    yesterday = datetime.now() - timedelta(days=days)

    # Format the date as YYYYMMDD
    return yesterday.strftime("%Y%m%d")


# def clean_mark_column(df: pd.DataFrame) -> pd.DataFrame:
#     """this function will remove rows if the mark column is not a number"""
#     # return df[pd.to_numeric(df["Mark"], errors="coerce").notna()]
#     return df["Mark"] = df["Mark"].fillna(value=0)


def calc_option_premium(df: pd.DataFrame) -> pd.DataFrame:
    # Create a boolean mask for rows where "Security" contains "(Warr)"
    is_warrant = df["Security"].str.contains(r"\(Warr\)", regex=True)
    
    # Apply calculations based on the mask
    df["OptionPremium"] = df["Quantity"] * df["Mark"] * 1  # Default multiplier for warrants is 1
    df.loc[~is_warrant, "OptionPremium"] *= 100 # Non-warrants
    
    return df


# def sum_option_premium(df: pd.DataFrame) -> pd.DataFrame:
#     return int(df["OptionPremium"].apply(lambda x: x if isinstance(x, int) else 0).sum())


# def sum_short_option_premium(df: pd.DataFrame) -> pd.DataFrame:
#     return int(df["OptionPremium"].apply(lambda x: x if isinstance(x, int) and x < 0 else 0).sum())


# def sum_long_option_premium(df: pd.DataFrame) -> pd.DataFrame:
#     return int(df["OptionPremium"].apply(lambda x: x if isinstance(x, int) and x > 0 else 0).sum())
