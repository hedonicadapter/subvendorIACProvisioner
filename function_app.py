import azure.functions as func
import subprocess
import logging
import os
from git import Repo
from models.stgAcc import RootRequestBody
from python_terraform import *
from openapi_schema_validator import validate
from dataclasses import dataclass
from urllib.parse import urlparse
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

iacDir = "/tmp/IAC"
tf = Terraform(working_dir=iacDir)

@dataclass
class RequestBody:
    contents: dict[str, str]

# 1. validate request data with openapi
def validateRequest(req: func.HttpRequest):
    try:
        version = req.route_params.get('version') or "versioning-not-implemented" # WARN: when versioning is implemented: or "latest"
        data = req.get_json()
        # req_body = RootRequestBody.from_dict(data)

        return func.HttpResponse(
            f"This HTTP body function executed successfully. {data}",
            status_code=200
        )
    except ValueError as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)
    except TypeError as e:
        return func.HttpResponse(f"Missing required field: {str(e)}", status_code=400)
    else:
        spec_url = f"https://apigeneratoridiotms.blob.core.windows.net/api-gen/{version}.json"
        response = requests.get(spec_url)
        if response.status_code != 200:
            return func.HttpResponse(f"Failed to fetch API spec: {response.status_code}", status_code=400)
        spec_dict = response.json()

        return func.HttpResponse(
            f"This HTTP bungus function executed successfully. {spec_dict}",
            status_code=200
        )
    
# 2. clone repo
def cloneIACRepo():
    repo_url = "https://github.com/hedonicadapter/terraform-modules.git"
    logging.info(f"Cloning repository from {repo_url}.")

    repo = Repo.clone_from(repo_url, iacDir)
    logging.info(f"Repository cloned successfully: {repo}.")

def initializeDirectory():
    logging.info("Removing existing IAC directory.")
    _ = subprocess.run(["rm", "-rf", iacDir])

    logging.info("Upserting tmp IAC directory")
    os.makedirs(iacDir, exist_ok=True)

# 3. provision IAC
def terraformInit():
    tf.init()

def terraformPlan():
    tf.plan()

def terraformApply():
    tf.apply()


@app.route(route="requestSubscription/{version}")
def requestSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("requestSubscription function triggered.")
    try:
        validation_response = validateRequest(req)
        if isinstance(validation_response, func.HttpResponse):
            return validation_response
        # initializeDirectory()
        # cloneIACRepo()
        # terraformInit()
        # terraformPlan()
        # terraformApply()

        path = urlparse(req.url).path

        return func.HttpResponse(
            f"This HTTP chungus function executed successfully. {path}",
            status_code=200
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        return func.HttpResponse(
            "Internal Server Error: Subprocess failed.",
            status_code=500
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )
