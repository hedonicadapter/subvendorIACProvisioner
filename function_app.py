import azure.functions as func
import subprocess
import logging

from git import Repo
from python_terraform import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# validate request data with openapi and apim

# run terraform init && terraform plan
# tf = Terraform(working_dir='./IAC', variables={'a':'b', 'c':'d'})
# tf.apply()

@app.route(route="createSubscription")
def createSubscription(req: func.HttpRequest) -> func.HttpResponse:
    # clone IAC repo
    subprocess.run(["rm", "-rf", "./IAC"]) 
    repo_url = "https://github.com/hedonicadapter/terraform-modules.git"
    repo = Repo.clone_from(repo_url, "./IAC")
    print(repo)

    return func.HttpResponse(
         "This HTTP triggered function executed successfully.",
         status_code=200
    )
