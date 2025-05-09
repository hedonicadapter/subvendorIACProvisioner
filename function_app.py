import azure.functions as func
import logging

from git import Repo

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# validate request data with openapi and apim

# clone IAC repo
# repo_url = "https://github.com/hedonicadapter/terraform-modules.git"
# repo = Repo.clone_from(repo_url, "./IAC")

# run terraform init && terraform plan
# from python_terraform import *
# tf = Terraform(working_dir='./IAC', variables={'a':'b', 'c':'d'})
# tf.apply()

@app.route(route="createSubscription")
def createSubscription(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
         "This HTTP triggered function executed successfully.",
         status_code=200
    )
