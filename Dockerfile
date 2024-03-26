FROM bitnami/spark:latest

COPY app.py /opt/bitnami/spark/app.py
COPY requirements.txt /opt/bitnami/spark/requirements.txt

RUN pip install -r /opt/bitnami/spark/requirements.txt

ENV SPARK_MASTER_URL=spark://spark-master:7077

CMD ["spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/app.py"]