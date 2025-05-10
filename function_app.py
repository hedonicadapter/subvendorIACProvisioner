import azure.functions as func
import subprocess
import logging
from git import Repo
from python_terraform import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="createSubscription")
def createSubscription(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("createSubscription function triggered.")
    try:
        logging.info("Removing existing IAC directory.")
        subprocess.run(["rm", "-rf", "/tmp/IAC"])

        repo_url = "https://github.com/hedonicadapter/terraform-modules.git"
        logging.info(f"Cloning repository from {repo_url}.")

        repo = Repo.clone_from(repo_url, "/tmp/IAC")
        logging.info(f"Repository cloned successfully: {repo}.")

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
