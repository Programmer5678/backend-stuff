from fastapi import APIRouter
from .base_models import PathsRequestModel, CreatedResponseModel
from src.encode.encode import encode
from src.decode.decode import decode

router = APIRouter( prefix="/main")

@router.post(
    "/encode",
    response_model = CreatedResponseModel
)
def encodeRoute( paths : PathsRequestModel):
    encode(paths.input_path, paths.output_path)
    return {"created" : paths.output_path}


@router.post(
    "/decode",
    response_model = CreatedResponseModel
)
def decodeRoute( paths : PathsRequestModel):
    decode(paths.input_path, paths.output_path)
    return {"created" : paths.output_path}

