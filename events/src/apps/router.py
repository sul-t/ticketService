from fastapi import APIRouter, Request


router = APIRouter(prefix='/events', tags=['Events'])

@router.get('')
async def get_request(request: Request):
    return {"message": 'yeap'}