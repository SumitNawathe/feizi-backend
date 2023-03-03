FROM python:3.7

RUN apt-get update && apt-get install -y postgresql

EXPOSE 8000

COPY . backend

ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000

WORKDIR backend
RUN pip install .

ENTRYPOINT flask run
