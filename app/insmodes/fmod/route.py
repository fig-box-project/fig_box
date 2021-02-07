from fastapi import APIRouter

bp = APIRouter()

@bp.get("/routeA")
def test():
    pass