from flask import Blueprint

health_bp = Blueprint("Health", __name__)
palindromes_bp = Blueprint("Palindromes", __name__)

from . import health  # noqa: F401
from . import palindromes  # noqa: F401
