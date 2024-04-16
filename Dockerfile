FROM python:3.10
WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn 

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]