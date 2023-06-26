import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv()

SECRET_KEY = get_random_secret_key()
DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("MYSQL_ROOT_PASSWORD"),
        "PORT": "3306",
        "OPTIONS": {"autocommit": True},
    }
}
