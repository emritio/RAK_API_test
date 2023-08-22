FROM python:3.8

RUN pip install Flask
RUN pip install psycopg2
RUN pip install flask_sqlalchemy
ENV DATABASE_URL=postgresql://postgres:123@my-postgres/postgres
WORKDIR /app

COPY apilog.py apilog.py        

CMD ["python3", "apilog.py"]