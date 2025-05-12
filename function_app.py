import azure.functions as func
import subprocess
import logging
import os
from git import Repo
from python_terraform import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

iacDir = "/tmp/IAC"
tf = Terraform(working_dir=iacDir)

# 1. validate request data with openapi and apim
def validateRequest(req: func.HttpRequest):
   raise NotImplementedError("not implemented")

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
        version = req.route_params.get("version")
        print(version)
        # validateRequest(req)
        initializeDirectory()
        cloneIACRepo()
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
