import azure.functions as func
import datetime
import json
import logging
import traceback

app = func.FunctionApp()

@app.function_name(name="httpTrigger")
@app.route(route="createSubscription", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def createSubscription(req: func.HttpRequest) -> func.HttpResponse:
    try:
        print(req.headers.get('Api-Version'))
    except ValueError as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)

    return func.HttpResponse(
        status_code=200,
    )

