import flask
from flask import request ,jsonify, Flask, make_response
from flask.logging import default_handler
from flask_restful import Api
import logging
import api_types
import ecs_logging
import business_service
import json
import api_errors

# Get the Logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

app = flask.Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True
app.logger.propagate = False
logger.propagate = False


# Add an ECS formatter to the Handler
handler = logging.StreamHandler()

formatter = ecs_logging.StdlibFormatter(
    exclude_fields=[
        # You can specify individual fields to ignore:
        "log.original",
        # or you can also use prefixes to ignore
        # whole categories of fields:
        "process",
        "log.origin",
    ]
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# GET /customers resource - returns a collection of Customers
@app.route('/customers', methods=['GET'])
def api_get_customers():
    logger.info("Info level message log in / route.")
    custs =  business_service.get_customers()
    cust_schema = api_types.CustomerSchema(many=True)
    cust_json = cust_schema.dump(custs)

    response = make_response(json.dumps(cust_json), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

# POST /customers resource - provisions a new Customer
@app.route('/customers', methods=['POST'])
def api_post_customers():
    logger.info("Info level message log in / route.")
    cust = business_service.create_customer()
    cust_schema = api_types.CustomerSchema()
    cust_json = cust_schema.dump(cust)
    response = make_response(json.dumps(cust_json), 201,)
    response.headers['location'] = "/customers/{customerId}".format(customerId=cust.customer_id)
    return response

# GET /customers/<customerId> - returns a specific customer by ID
@app.route('/customers/<customerId>', methods=['GET'])
def api_get_customer(customerId):
    logger.info("Retrieving customer by ID.")
    cust = business_service.get_customer(customerId)
    cust_schema = api_types.CustomerSchema()
    cust_json = cust_schema.dump(cust)
    response = make_response(json.dumps(cust_json), 200,)
    return response


### Register Error Handlers

@app.errorhandler(api_errors.ConflictException)
def handle_conflict_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(api_errors.ServerError)
def handle_server_err_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(api_errors.NotFoundException)
def handle_not_found_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.run()
