FROM python:3.8

RUN pip install Flask
RUN pip install psycopg2
RUN pip install flask_sqlalchemy
RUN pip install bcrypt
WORKDIR /app

COPY apilog.py apilog.py        

CMD ["python3", "apilog.py"]