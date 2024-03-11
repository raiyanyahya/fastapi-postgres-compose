# Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./app /code/app
COPY requirements.txt /code/
COPY .env /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]