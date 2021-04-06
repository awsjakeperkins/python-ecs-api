
from flask import request, Response, jsonify

import logging
import uuid
import marshmallow.validate
from dataclasses import dataclass, field
import dataclasses
from typing import List, Optional
import api_types
import api_errors

from marshmallow import Schema, INCLUDE, fields, EXCLUDE, post_dump, post_load

"""Business Layer for Sample API"""

# In-Memory Map for transient storage
backend_map = {}
# Init 1 customer

logger = logging.getLogger("app")


# Business Logic tier for retrieving all customers
def get_customers():

    custs = []
    for cust in backend_map.values():
        custs.append(cust)
    print(custs)
    return custs

# Business Logic Tier for retrieving a customer by ID
def get_customer(id) -> api_types.Customer:
    
    if id in backend_map:
        return backend_map[id] 
    else:
        err_msg = "No Customer exists for for id %s" % (id)
        logger.warn(err_msg)
        raise api_errors.NotFoundException(err_msg)

# Business Logic tier for provisioning a new customer
def create_customer() -> api_types.Customer:

    logger.info("Creating new Client")

    print(request.json)
    json_request = request.json
    logging.info(json_request)

    schema = api_types.CustomerSchema()
    customer = schema.load(json_request)
    customer.customer_id = str(uuid.uuid4())

    backend_map[customer.customer_id] = customer

    logger.info("Provisioned Client with ID : %s" % customer.customer_id)

    return customer

    



