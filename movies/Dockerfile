FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir


RUN pybabel extract -F babel.cfg -k _l -o messages.pot .
RUN pybabel init -i messages.pot -d translations -l en
RUN pybabel init -i messages.pot -d translations -l ru

RUN pybabel compile -d translations

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000