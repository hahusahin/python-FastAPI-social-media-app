from passlib.context import CryptContext

# Tells passlib that we want to use Bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
