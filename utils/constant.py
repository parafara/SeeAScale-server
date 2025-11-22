from dotenv import load_dotenv
import os

load_dotenv()

# global
RELEASE = not os.getenv("RELEASE") is None

# format
EMAIL_FORMAT = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
USER_NAME_FORMAT = r"^[가-힣A-Za-z0-9_]{1,16}$"
THING_NAME_FORMAT = r"^[가-힣A-Za-z0-9_]{1,32}$"
PASSWORD_FORMAT = r"^[A-Za-z0-9!@#$-_.?]{8,}$"

# constant record
PREREGISTER_EXPIRY_PERIOD = 10 * 60
LOGIN_EXPIRY_PERIOD = 24 * 60 * 60

# database
DB_URL = os.getenv("DB_URL")

# token_manager
JWT_KEY = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# crypto_tools
HASH_PAPPER = os.getenv("HASH_PAPPER").encode()
HASH_ID_SALT = os.getenv("HASH_ID_SALT")