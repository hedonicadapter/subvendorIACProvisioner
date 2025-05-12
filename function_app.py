import azure.functions as func
import subprocess
import logging
import os
from git import Repo
from python_terraform import *
from openapi_schema_validator import validate
from dataclasses import dataclass
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
        req_body = RequestBody(**data)
    except ValueError as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)
    except TypeError as e:
        return func.HttpResponse(f"Missing required field: {str(e)}", status_code=400)
    else:
        spec_url = f"https://apigeneratoridiotms.blob.core.windows.net/api-gen/{version}.json"
        response = requests.get(spec_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch API spec: {response.status_code}")
        spec_dict = response.json()

        logging.info(spec_dict)
        return func.HttpResponse(
            f"This HTTP triggered function executed successfully. {spec_dict}",
            status_code=200
        )
    
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


@app.route(route="requestSubscription/{version}")
def requestSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("requestSubscription function triggered.")
    try:
        validateRequest(req)
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
