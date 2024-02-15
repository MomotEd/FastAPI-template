FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./app /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

ENV APP_MODULE=app.main:app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]