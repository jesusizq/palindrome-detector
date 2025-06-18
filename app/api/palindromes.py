import uuid
from flask import url_for
from apifairy import arguments, body, response
from app.api import palindromes_bp as api
from app.api.schemas import (
    EmptySchema,
    PalindromeCreateSchema,
    PalindromeListSchema,
    PalindromeQuerySchema,
    PalindromeSchema,
)
from app.extensions import cache
from app.services import palindrome_service
from app.services.palindrome.palindrome_dtos import (
    PalindromeCreateDTO,
    PalindromeQueryDTO,
)


@api.route("", methods=["POST"])
@body(PalindromeCreateSchema)
@response(PalindromeSchema, 201)
def create(data):
    """Try to create a new palindrome"""
    palindrome_dto = PalindromeCreateDTO(**data)
    palindrome = palindrome_service.create(palindrome_dto)
    return palindrome


@api.route("/<uuid:palindrome_id>", methods=["GET"])
@response(PalindromeSchema)
def get_by_id(palindrome_id: uuid.UUID):
    """Retrieve a palindrome by id"""
    return palindrome_service.get_by_id(palindrome_id)


@api.route("", methods=["GET"])
@arguments(PalindromeQuerySchema)
@response(PalindromeListSchema)
@cache.cached()
def get_palindromes(args):
    """Retrieve a list of palindromes"""
    query_dto = PalindromeQueryDTO(**args)
    pagination = palindrome_service.get_all(query_dto)

    url_args = args.copy()
    url_args.pop("page", None)

    prev_url = (
        url_for("Palindromes.get_palindromes", page=pagination.prev_num, **url_args)
        if pagination.has_prev
        else None
    )
    next_url = (
        url_for("Palindromes.get_palindromes", page=pagination.next_num, **url_args)
        if pagination.has_next
        else None
    )

    return {
        "items": pagination.items,
        "prev_url": prev_url,
        "next_url": next_url,
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page,
        "per_page": pagination.per_page,
    }


@api.route("/<uuid:palindrome_id>", methods=["DELETE"])
@response(EmptySchema, 204)
def delete(palindrome_id: uuid.UUID):
    """Delete a palindrome"""
    palindrome_service.delete_by_id(palindrome_id)
    return {}
