from datetime import datetime, timedelta

import pandas as pd


def get_date(days: int) -> str:
    yesterday = datetime.now() - timedelta(days=days)

    # Format the date as YYYYMMDD
    return yesterday.strftime("%Y%m%d")


def get_wf_lending_rate_final(wf_lending_rate: pd.DataFrame, gc: float) -> pd.DataFrame:
    df = wf_lending_rate.copy()
    df.loc[df["Rate"] == "GC", "Rate"] = gc
    # df['Altered Rate'] = df['Rate'] * gc
    return df


def calculate_borrow_rate(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df_merged = pd.merge(df1, df2, left_on="Symbol", right_on="Ticker")
    df_merged["Rate"] = pd.to_numeric(df_merged["Rate"], errors="coerce")
    df_merged["Borrow Cost"] = df_merged["Quantity"] * df_merged["Rate"] / 100
    df_merged["Borrow Cost"] = df_merged["Borrow Cost"].round().astype(int)
    df_sorted = df_merged.sort_values(by="Borrow Cost", ascending=True, na_position="last")
    df_sorted = df_sorted.drop(columns=["Ticker", "AvailableQty", "Sedol", "Cusip", "ISIN"])
    return df_sorted


def filter_df_for_negative_borrow_rate(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Borrow Cost"] <= 0]


def get_tickers_with_long_stock_but_no_rate_found(df_wf_summed, df_wf_final) -> pd.DataFrame:
    # gets the rows in df1 that are not in df2
    diff_df = df_wf_summed.merge(df_wf_final, how="left", indicator=True)

    # filter for rows that are only in df1
    return diff_df[diff_df["_merge"] == "left_only"].drop(columns="_merge")
