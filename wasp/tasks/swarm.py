
from pyspark.sql.session import SparkSession
from pyspark.sql import DataFrame


from wasp.common.data_reader import DataReader
from wasp.config import settings
from wasp.common import utils

import pendulum
from pyspark.sql.functions import lit, to_date, to_utc_timestamp

def extract_participants(spark: SparkSession) -> DataFrame:
    """Extract participants data from Tower of Truth.

    The following transformations are applied:

    #. ``valid_from`` is set to the date of ``loaded_at``, after converting it to the
       local time zone specified in ``swarm.flows.timezone``.
    #. ``valid_to`` is set to the maximum date of ``9999-12-31``.

    Returns:
        A :py:class:`dask.dataframe.DataFrame` conforming to
        :py:data:`cuebox.swarm.schema.participants`, with "id" replicated as the index.
    """

    data_reader = DataReader(
        spark=spark,
        tower_url=settings.swarm.tower.url,
        category="profile",
        name="participants",
    )
    df = data_reader.get_all_data()
    df = df.select("id", "first_name", "last_name", "loaded_at")
    tz = utils.tz()

    result_df = df.withColumn(
        "valid_from", lit(to_date(to_utc_timestamp(df.loaded_at, tz=tz)))
    ).drop("loaded_at")
    result_df = result_df.withColumn(
        "valid_to", lit(pendulum.from_format(utils.max_date(), fmt="YYYY-MM-DD").date())
    )

    return result_df