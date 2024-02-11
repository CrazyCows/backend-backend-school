from fastapi import APIRouter

# Just an example of how to setup routing for CRUD

router = APIRouter()

@router.post("/hi/")
async def test_post():
    return

@router.get("/hi/")
async def test_get():
    return

@router.options("/hi/")
async def test_options():
    return

@router.delete("/hi/")
async def test_delete():
    return
