from io import StringIO

import boto3
import pandas as pd

from src.settings import MS_BUCKET, WF_BUCKET
from src.utils.utils_func import get_date

s3 = boto3.client("s3")


def get_wf_lending_rates(s3) -> pd.DataFrame:
    yesterday = get_date(1)
    wf_filepath = f"{yesterday}/Availability_WF_Caption_{yesterday}.csv"

    # Download the CSV file as a string
    response = s3.get_object(Bucket=WF_BUCKET, Key=wf_filepath)
    csv_data = response["Body"].read().decode("utf-8")

    # Convert the CSV string to a DataFrame
    df = pd.read_csv(StringIO(csv_data))

    # for debugging in the future
    print(df.head())

    return df


def get_gc_rate_from_ms(s3) -> float:
    today = get_date(0)
    yesterday = get_date(1)
    ms_filepath = f"{today}/IN150DX-038CACOK3.{yesterday}.csv"
    # Download the CSV file as a string
    response = s3.get_object(Bucket=MS_BUCKET, Key=ms_filepath)
    csv_data = response["Body"].read().decode("utf-8")

    # Convert the CSV string to a DataFrame
    df = pd.read_csv(StringIO(csv_data))

    return df["Base Rate"][0] - 0.30
