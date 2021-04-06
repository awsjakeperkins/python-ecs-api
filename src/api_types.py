
from flask import request, Response, jsonify

import logging
import uuid
import marshmallow.validate
from dataclasses import dataclass, field
import dataclasses
from typing import List, Optional

from marshmallow import Schema, INCLUDE, fields, EXCLUDE, post_dump, post_load

@dataclass
class Customer:
    customer_id: str = field(default='')
    customer_name: str = field(default='')

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


class CustomerSchema(Schema):
    """ Schema for Application object serialization/deserialization """

    customer_id = fields.String(default="", data_key="CustomerId")
    customer_name = fields.String(default="", data_key="CustomerName")


    # Ignore unrecognized field attributes
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)