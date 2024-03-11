# Dockerfile
FROM python:3.9

RUN apt update -y && apt-get update -y && apt-get install --no-install-recommends -y sudo git curl wget nano lsof && \
        rm -rf /var/lib/apt/lists/* && \
	      apt-get clean && \
        apt-get autoclean && \
        apt-get autoremove
        
WORKDIR /code

COPY ./app /code/app
COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
