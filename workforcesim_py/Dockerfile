FROM python:3.10.9

RUN mkdir /code

WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "wfs_app:app", "--host=0.0.0.0", "--port=80"]