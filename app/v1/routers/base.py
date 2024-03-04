from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
def health_check():
    return {"message": "It works"}
