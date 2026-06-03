import azure.functions as func
import logging
from azure.data.tables import TableServiceClient
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetVisitorCount")
def GetVisitorCount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Visitor counter function processed a request.')

    try:
        # Connect to CosmosDB Table
        conn_str = os.environ["COSMOS_CONNECTION_STRING"]
        client = TableServiceClient.from_connection_string(conn_str)
        table = client.get_table_client("counter")

        # Get the current count
        entity = table.get_entity(partition_key="1", row_key="1")
        count = int(entity["counter"]) + 1

        # Update the count
        entity["counter"] = count
        table.update_entity(entity)

        # Return the new count
        return func.HttpResponse(
            json.dumps({"count": count}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )