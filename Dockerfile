FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y terraform && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot
