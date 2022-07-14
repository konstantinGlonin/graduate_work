FROM python:3.10-slim

WORKDIR /app/elt/elastic

COPY . /app/elt/elastic

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN pip install -r requirements.txt

RUN python --version
CMD python load_data.py