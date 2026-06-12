from passlib.context import CryptContext
from prisma import Prisma

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(client: Prisma, email: str):
    return await client.user.find_unique(where={"email": email})


async def create_user(client: Prisma, email: str, password: str, name: str | None = None, organization_id: str | None = None):
    hashed_password = hash_password(password)
    user = await client.user.create(
        data={
            "email": email,
            "hashedPassword": hashed_password,
            "name": name,
            "organization": organization_id and {"connect": {"id": organization_id}} or None,
        }
    )
    return user
