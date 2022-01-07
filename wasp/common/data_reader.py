import datetime
import posixpath
from typing import Optional, Union
from pathlib import Path

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from wasp.common import utils


class DataReader:
    """Reader for tower of truth data"""

    def __init__(
        self, spark: SparkSession, tower_url: str, category: str, name: str
    ) -> None:
        """
        Args:
            tower_url: fsspec-compatible URL to Tower of Truth.
            category: The category of the table, e.g. "profile".
            name: The name of the table, e.g. "participants".
        """
        self.spark = spark
        self.tower_url = tower_url
        self.category = category
        self.name = name

    def exists(self) -> bool:
        return True

    @property
    def table_url(self) -> str:
        """URL for the table within Tower of Truth."""
        return posixpath.join(self.tower_url, self.category, self.name)

    def get_all_data(self) -> DataFrame:
        df = self.spark.read.parquet(self.table_url)
        return df

    def get_data(
        self, num_of_days: int = 0, end_date: Optional[datetime.date] = None
    ) -> DataFrame:
        """Extract the latest dates of data from the table.

        This is useful for fact tables, where a limited number of dates of data is
        required, e.g. last 7 days or last 30 days.

        Args:
            num_of_days: Number of days of data to extract.
            end_date: The last date of data to extract. If not specified, the current
                date in the configured flows timezone is used.

        Returns:
            The extracted data.
        """
        filter_end_date = utils.date_or_today(end_date)
        filter_start_date = filter_end_date.subtract(days=num_of_days - 1)
        df = self.spark.read.parquet(self.table_url).filter(
            f"partition_date >= '{filter_start_date}' AND partition_date <= '{filter_end_date}'"
        )
        return df
