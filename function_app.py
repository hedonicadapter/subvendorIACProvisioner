import azure.functions as func
import subprocess
import logging
import os
from git import Repo
from models.stgAcc import RootRequestBody
from models.error import APIValidationError
from python_terraform import *
from openapi_schema_validator import validate
from urllib.parse import urlparse
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

iacDir = "/tmp/IAC"

def getAPISchema(version: str):
    spec_url = f"https://apigeneratoridiotms.blob.core.windows.net/api-gen/{version}.json"

    response = requests.get(spec_url)
    if response.status_code != 200:
        raise APIValidationError(f"Failed to fetch API spec from {spec_url}: {response.status_code}", status_code=500)

    spec_dict = response.json()
    return RootRequestBody.from_dict(spec_dict)

# 1. validate request with API schema
def validateRequest(path:str, req_data:dict[str,str], schema:RootRequestBody):
    for k, v in schema.paths.items():
        if k == path:
            return validate(req_data, v.post.requestBody.content.application_json.schema)

    raise APIValidationError("Schema validation failed.", status_code=500)
    
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
    tf = Terraform(working_dir=iacDir)
    tf.init()

def terraformPlan():
    tf.plan()

def terraformApply():
    tf.apply()


@app.route(route="requestSubscription/{version}")
def requestSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("requestSubscription function triggered.")
    try:
        version = req.route_params.get('version') or "versioning-not-implemented"
        path = urlparse(req.url).path.removeprefix("/api").removesuffix("/" + version)
        req_data = req.get_json()
        schema = getAPISchema(version)
        logging.info(req_data)

        validateRequest(path, req_data, schema)
        initializeDirectory()
        cloneIACRepo()
        terraformInit()
        # terraformPlan()
        # terraformApply()

        return func.HttpResponse(
            f"This HTTP chungus function executed successfully. {req_data}",
            status_code=200
        )
    except APIValidationError as e:
        return func.HttpResponse(e.message, status_code=e.status_code)
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
