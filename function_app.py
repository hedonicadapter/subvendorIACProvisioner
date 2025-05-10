import azure.functions as func
import subprocess
import logging
import os
from git import Repo
from python_terraform import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def cloneIACRepo():
    repo_url = "https://github.com/hedonicadapter/terraform-modules.git"
    logging.info(f"Cloning repository from {repo_url}.")

    repo = Repo.clone_from(repo_url, "/tmp/IAC")
    logging.info(f"Repository cloned successfully: {repo}.")

def initializeDirectory():
    logging.info("Removing existing IAC directory.")
    _ = subprocess.run(["rm", "-rf", "/tmp/IAC"])

    logging.info("Upserting tmp IAC directory")
    os.makedirs("/tmp/IAC", exist_ok=True)

@app.route(route="createSubscription")
def createSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("createSubscription function triggered.")
    try:
        initializeDirectory()
        cloneIACRepo()

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
