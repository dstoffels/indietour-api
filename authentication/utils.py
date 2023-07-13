import secrets
import string
from rest_framework.response import Response


def generate_verification_code():
    chars = string.digits
    return "".join(secrets.choice(chars) for _ in range(6))


def generate_password():
    chars = [*string.ascii_letters, *string.digits]
    return "".join(secrets.choice(chars) for _ in range(12))
