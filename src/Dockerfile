FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y make automake gcc g++ subversion python3-dev
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./ /src
WORKDIR /src
EXPOSE 8000/tcp

CMD /wait && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app