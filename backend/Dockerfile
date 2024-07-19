FROM python:3.10-slim-buster
LABEL authors="ronylitv"

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && mkdir "models"


COPY . .
EXPOSE 8000
EXPOSE 6379

ENTRYPOINT ["fastapi", "run", "main.py", "--host" , "0.0.0.0", "--port", "8000"]

