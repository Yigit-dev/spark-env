# Apache Spark Environment with Docker

## Pyspark

```
cd pyspark
docker build -t pyspark-app .
docker run pyspark-app
```

## Jupyter Notebook

```
cd jupyter
docker-compose up --build
or
docker-compose up
```

## WEB APP

```
cd web-app
docker-compose up --build
or
docker-compose up
```

Once the application runs it will here http://127.0.0.1:8000/

### Create New project

```
docker-compose run web django-admin startproject <project-name> .
docker-compose up
```

### Start App

```
docker-compose run web python manage.py startapp <app_name>
docker-compose up --build
```
