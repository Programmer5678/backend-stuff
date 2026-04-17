from fastapi import APIRouter
from .base_models import PathsRequestModel
from src.encode.encode import encode
from src.decode.decode import decode

router = APIRouter( prefix="/main")

@router.post(
    "/encode"
)
def encodeRoute( paths : PathsRequestModel):
    encode(paths.input_path, paths.output_path)


@router.post(
    "/decode"
)
def decodeRoute( paths : PathsRequestModel):
    decode(paths.input_path, paths.output_path)

