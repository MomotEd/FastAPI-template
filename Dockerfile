FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./app /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r ./requirements.txt

ENV APP_MODULE=app.main:app

EXPOSE 8000

CMD ["python", "webservice.py", "--reload"]