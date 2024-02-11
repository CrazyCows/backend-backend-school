from pathlib import Path
from passlib.context import CryptContext
from models.auth import Token
import jwt

# just setting the path to the root of the folder for easily tetsing...
script_path = Path(__file__).parent

private_key_path = script_path.parent / "verification/private_key.pem"
public_key_path = script_path.parent / "verification/public_key.pem"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "RS256"

with open(private_key_path, "r") as key_file:
    PRIVATE_KEY = key_file.read()

with open(public_key_path, "r") as key_file:
    PUBLIC_KEY = key_file.read()


# Data in the token we can retrieve upon revival
def create_access_token() -> Token:
    to_encode = {"user_id": 123, "username": "example_user"}
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return Token(token=encoded_jwt)


def decode_token(token: Token) -> str:
    # write code to decode the token again
    decoded_jwt = jwt.decode(token)
    return decoded_jwt
