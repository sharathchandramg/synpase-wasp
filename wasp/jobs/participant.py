
import sys, os

# sys.path.append(os.getcwd())

from pyspark.sql.session import SparkSession
from wasp.common import utils
from wasp.tasks.swarm import extract_participants

def main(args):
    spark = SparkSession.builder.appName("wasp").getOrCreate()
    print(f"The version is {spark.version}")
    print(f"\n".join(sys.path))
    
    participants_df = extract_participants(spark)
    participants_df.show()
    # upsert_participants.run(data=participants_df, mode="append", password=db_pw)


if __name__ == "__main__":
    main(sys.argv)
