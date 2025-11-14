from fastapi.security import HTTPBearer
from fastapi import HTTPException,status
from src.auth.utils import decode_token
from fastapi import Request
from src.db.redis import token_in_blocklist, add_token_to_blocklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                'error': 'This token is invalid or been revoke',
                'resolution' :'Please get a new token'
            })
        # ensure token_data contains a jti
        jti = None
        if isinstance(token_data,dict):
            jti = token_data.get('jti')

        if not jti:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                'error': 'This token is invalid or been revoke',
                'resolution': 'Please get a new token'
            })

        # check blocklist using the helper function
        if await token_in_blocklist(jti):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                'error': 'This token is invalid or been revoke',
                'resolution' :'Please get a new token'
            })

            
        self.verify_token_data(token_data)

        return token_data
        
    def token_valid(self, token: str) -> bool:
        decode = decode_token(token)
        return  decode is not None 
    
    def verify_token_data(self, token_data):
        raise NotImplementedError('Please override this method in the child class')
    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict) -> None:
        # treat missing 'refresh' as False
        if token_data and token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                  detail="Please provide access token.")
        

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict) -> None:
        # treat missing 'refresh' as False
        if token_data and not token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                  detail="Please provide a valid refresh token .") 
        
