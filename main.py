from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper

app = FastAPI()

inprogress_orders = {}


@app.post("/")
async def handle(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    intent_handler_dict = {
        "order.add-context:ongoing-order": add_to_order,
        "track.order-context:ongoing-tracking": track_order

    }
    return intent_handler_dict[intent](parameters)


def add_to_order(parameters: dict):
    food_items = parameters["food-item"]
    quantities = parameters["number"]
    if len(food_items) != len(quantities):
        fulfillment_text = f"Sorry I didn't Understand. Can you please specify food items and quantities clearly"
    else:
        fulfillment_text = f"Received {food_items} and {quantities} in the backend"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters: dict):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id {order_id}"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
