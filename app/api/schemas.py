from marshmallow import fields
from app.extensions import ma


class HealthSchema(ma.Schema):
    status = fields.String(
        required=True,
        metadata={
            "description": "Indicates the health status of the service.",
            "example": "ok",
        },
    )
