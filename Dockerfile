# Using parent image with minimal python packages
# Using python 3.10
FROM python:3.10-slim

MAINTAINER Gershon Shif "<gershon@levelops.io>"

COPY . Chatbot

RUN pip install --no-cache-dir pytest==6.2.5
RUN pip install --no-cache-dir python-dateutil==2.8.2
RUN pip install --no-cache-dir pytest-html==3.1.1
RUN pip install --no-cache-dir pytest-metadata==1.11.0
RUN pip install --no-cache-dir websocket-client==1.2.3

WORKDIR Chatbot
RUN cp scripts/run_master.py .
RUN cp scripts/run_tests.sh .
RUN chmod +x run_master.py

ENTRYPOINT ["bash", "run_tests.sh"]
