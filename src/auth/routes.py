from click import confirm
from fastapi import APIRouter, Depends,HTTPException,status
from sqlmodel.ext.asyncio.session import AsyncSession
from . schemas import CreateUser , UserResponds, Login,Reset_password
from src.db.main import get_db
from . service import AuthService
from . utils import create_token
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from . depencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_token_to_blocklist


auth_router = APIRouter()
user_service = AuthService()
REFRESH_TOKEN_EXPIRE_DAYS = 2
@auth_router.post("/signup",response_model= UserResponds, status_code=status.HTTP_201_CREATED)
async def new_user(user_data:CreateUser,session:AsyncSession = Depends(get_db)):
    email = user_data.email
    user_exist = await user_service.user_exist(email,session)
    if user_exist :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="email already exist")
    else:
        user = await user_service.create_user(user_data,session)
        return user

#checking token generation and decoding
@auth_router.post("/login/token")
async def generate_token(login_data:Login, session:AsyncSession = Depends(get_db)):
    email = login_data.email
    password = login_data.password
    user = await user_service.user_exist(email,session)
    if user is not None:
        is_password_valid = await user_service.password_verify(password, user.password_hash)
        if is_password_valid:
            access_token = create_token(user_data={
                "uid": str(user.uid),
                "email": user.email,
            })
            
            refresh_token = create_token(user_data={
                "uid": str(user.uid),
                "email": user.email,
           }
            , refresh=True, expire_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
            return JSONResponse(content =
                                {"message" : "Login successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "email": user.email,
                       
                    }
                }
            )
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
            
        
               
@auth_router.get('/refresh_token')
async def get_new_access_token(token_deatils:dict = Depends(RefreshTokenBearer())):
    exprery_timestamp = token_deatils['exp']
    if datetime.fromtimestamp(exprery_timestamp)> datetime.now():
        new_access_token = create_token(
            user_data= token_deatils['user']
        )
        return JSONResponse(content={'access token':new_access_token})

    else:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST , detail="invalid access token")      

        

    
@auth_router.get('/logout')
async def revoke_token_data (token_details:dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_token_to_blocklist(jti)
    return JSONResponse( content={
        'message ':'Logged out successfully '}
        , status_code=status.HTTP_200_OK)


@auth_router.patch('/forgotten password')
async def forgotten_paassword(reset:Reset_password,session:AsyncSession = Depends(get_db)):
    email = reset.email
    confirm_password = await user_service.reset_password(email, reset, session)
    if confirm_password is None :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Email not matched')
    else:
        return confirm_password


    