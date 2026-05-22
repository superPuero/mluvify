from fastapi import APIRouter


router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"],
)


@router.get("/semantic")
async def analyze_semantic():
    pass


@router.get("/rithoric")
async def analyze_rithoric():
    pass
