FROM python:3.8

RUN pip install Flask
RUN pip install flask_sqlalchemy
RUN pip install bcrypt
RUN pip install flask_jwt_extended
RUN pip install datetime
RUN pip install psycopg2

WORKDIR /app

COPY . /app

CMD ["python3", "app.py"]
