FROM python:3.11

RUN pip install Flask
RUN pip install flask_sqlalchemy
RUN pip install bcrypt
RUN pip install flask_jwt_extended
RUN pip install datetime
RUN pip install psycopg2
RUN pip install apscheduler
RUN pip install psutil

WORKDIR /app

COPY . /app

CMD ["python3", "app.py"]
