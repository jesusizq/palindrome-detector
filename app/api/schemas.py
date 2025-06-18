from marshmallow import fields, validate
from app.extensions import ma


class HealthSchema(ma.Schema):
    status = fields.String(
        required=True,
        metadata={
            "description": "Indicates the health status of the service.",
            "example": "ok",
        },
    )


class PalindromeSchema(ma.Schema):
    id = fields.UUID(
        dump_only=True,
        metadata={"description": "The unique identifier of a palindrome detection."},
    )
    text = fields.Str(
        required=True, metadata={"description": "The text that was checked."}
    )
    language = fields.Str(
        required=True, metadata={"description": "The language of the text."}
    )
    is_palindrome = fields.Bool(
        dump_only=True, metadata={"description": "Whether the text is a palindrome."}
    )
    created_at = fields.DateTime(
        dump_only=True,
        metadata={"description": "The date and time when the detection was created."},
    )


class PalindromeCreateSchema(ma.Schema):
    text = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "The text to check for palindrome property."},
    )
    language = fields.Str(
        required=True,
        validate=validate.Length(equal=2),
        metadata={
            "description": "The language of the text (ISO 639-1 code, e.g., 'en', 'es')."
        },
    )


class EmptySchema(ma.Schema):
    pass


class PalindromeListSchema(ma.Schema):
    items = fields.List(fields.Nested(PalindromeSchema), data_key="palindromes")
    prev_url = fields.Str(dump_default=None)
    next_url = fields.Str(dump_default=None)
    total = fields.Int()
    pages = fields.Int()
    page = fields.Int()
    per_page = fields.Int()


class PalindromeQuerySchema(ma.Schema):
    language = fields.Str(
        required=False,
        validate=validate.Length(equal=2),
        metadata={"description": "Filter by language (ISO 639-1 code)."},
    )
    date_from = fields.Date(
        required=False, metadata={"description": "Filter by creation date (from)."}
    )
    date_to = fields.Date(
        required=False, metadata={"description": "Filter by creation date (to)."}
    )
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    page_size = fields.Int(
        load_default=50, data_key="per_page", validate=validate.Range(min=1)
    )
    sort = fields.Str(
        load_default="created_at",
        validate=validate.OneOf(["text", "language", "is_palindrome", "created_at"]),
    )
    order = fields.Str(load_default="desc", validate=validate.OneOf(["asc", "desc"]))
