from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, explode, split

spark = SparkSession.builder.appName("ReadAndPrintTxt").getOrCreate()

def clean_text(c):
    return lower(regexp_replace(c, '[^a-zA-Z\s]', '')).alias('cleaned')

df = spark.read.text("leipzig124MB.txt").select(clean_text(col("value")))

df = df.filter(col("cleaned") != "")

words = df.select(explode(split(col("cleaned"), "\s+")).alias("word"))

wordCounts = words.groupBy("word").count()

sortedWordCounts = wordCounts.orderBy(col("count").desc()).limit(10)

sortedWordCounts.show()

spark.stop()