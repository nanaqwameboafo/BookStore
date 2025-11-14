from . schemas import CreateUser
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from . models import User
from uuid import UUID
from . utils import Hash_password,verify_password


class AuthService:

    async def get_user_email(self, email:str , session:AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user_email =  result.first()
        return user_email

    async def password_verify(self, plain_password:str, hashed_password:str):
        return verify_password(plain_password, hashed_password)
    

    async def user_exist(self, email:str , session:AsyncSession):
        user = await self.get_user_email(email,session)
        return user if user is not None else None

    async def create_user(self , user_data:CreateUser, session : AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(
                **user_data_dict
            )

        new_user.password_hash = Hash_password(user_data_dict['password'])    

        session.add(new_user)
        await session.commit()
        return new_user

    