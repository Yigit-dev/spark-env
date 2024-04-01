from django.shortcuts import render
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, explode, split

# Create your views here.

def index(request):
    spark = SparkSession.builder.appName("ReadAndPrintTxt").getOrCreate()

    def clean_text(c):
        return lower(regexp_replace(c, '[^a-zA-Z\s]', '')).alias('cleaned')

    df = spark.read.text("./data/leipzig124MB.txt").select(clean_text(col("value")))

    df = df.filter(col("cleaned") != "")

    words = df.select(explode(split(col("cleaned"), "\s+")).alias("word"))

    wordCounts = words.groupBy("word").count()

    sortedWordCounts = wordCounts.orderBy(col("count").desc()).limit(10)

    # Spark DataFrame'den veriyi alarak bir liste oluşturun
    top_words_list = sortedWordCounts.collect()

    # Liste üzerinde döngü yaparak kelime ve sayı çiftlerini bir listeye ekleyin
    top_words = []
    for row in top_words_list:
        top_words.append((row['word'], row['count']))

    spark.stop()

    # Django şablonuna veriyi aktarın
    return render(request, 'index.html', {
        'top_words': top_words
    })

