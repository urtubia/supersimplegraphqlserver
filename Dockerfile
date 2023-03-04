FROM python:3.10 as base

RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# set the python path to include the current directory
ENV PYTHONPATH "${PYTHONPATH}:./src"

FROM base AS dev
RUN apt-get update && apt-get install -y iputils-ping
# make it run on port 8000 host 0.0.0.0
CMD uvicorn src.main:app --reload --log-level debug --port 8000 --host 0.0.0.0

FROM base AS tester
CMD python -m unittest discover -s tests -p 'test_*.py'

FROM tester AS final
CMD uvicorn src.main:app --port 8000 --host 0.0.0.0 --no-server-header
