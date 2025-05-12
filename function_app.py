import azure.functions as func
import requests
import subprocess
import logging
import os
from git import Repo
from python_terraform import *
from openapi_core import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from openapi_spec_validator import validate_spec
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

iacDir = "/tmp/IAC"
tf = Terraform(working_dir=iacDir)

# 1. validate request with openapi
# def validateRequest(req: func.HttpRequest):
#     version = req.route_params.get('version') or "versioning-not-implemented" # WARN: when versioning is implemented: or "latest"
#
#     spec_url = f"https://apigeneratoridiotms.blob.core.windows.net/api-gen/{version}.json"
#     response = requests.get(spec_url)
#     if response.status_code != 200:
#         raise ValueError(f"Failed to fetch API spec: {response.status_code}")
#     spec_dict = response.json()
#
#     validate_spec(spec_dict)
#
#     spec = create_spec(spec_dict)
#
#     # Convert Azure req to RequestsOpenAPIRequest
#     openapi_request = RequestsOpenAPIRequest(requests.Request(
#         method=req.method,
#         url=req.url,
#         headers=dict(req.headers),
#         params=dict(req.params),
#         data=req.get_body()
#     ))
#
#     result = RequestValidator(spec).validate(openapi_request)
#
#     result.raise_for_errors()

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

@app.route(route="requestSubscription", methods=[func.HttpMethod.POST])
def requestSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("requestSubscription function triggered.")
    try:
        # validateRequest(req)
        # initializeDirectory()
        # cloneIACRepo()
        # terraformInit()
        # terraformPlan()
        # terraformApply()

        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
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
