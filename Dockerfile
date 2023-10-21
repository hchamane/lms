FROM python:3.11.6-slim AS base

RUN apt-get update \
    && apt-get install gcc libc-dev musl-dev build-essential git iproute2 -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENV FLASK_APP=lms/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/app
ENV FLASK_RUN_PORT 5001

EXPOSE 5001
WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

FROM base AS debug
RUN python3 -m pip install debugpy -r tests/requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_DEBUG 1

ENTRYPOINT ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5001"]

FROM base AS tests
RUN python3 -m pip install -r tests/requirements.txt
ENV FLASK_ENV testing

ENTRYPOINT ["python3", "-m", "pytest"]

FROM base AS production
ENV FLASK_ENV production

ENTRYPOINT ["python3", "-m", "flask", "run"]