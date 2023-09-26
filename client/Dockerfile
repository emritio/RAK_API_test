FROM python:3.8

RUN pip install Flask
RUN pip install flask_sqlalchemy
RUN pip install bcrypt
RUN pip install flask_jwt_extended
RUN pip install datetime

WORKDIR /app

COPY apilog.py apilog.py        

CMD ["python3", "apilog.py"]
