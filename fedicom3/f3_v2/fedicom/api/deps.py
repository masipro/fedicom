
from typing import Dict
from fastapi import Header
from fastapi.responses import JSONResponse

from config import API_VERSION


def common_headers(
    software_id: str = Header(..., alias="Software-ID"),
    content_api_version: str = Header(..., alias="Content-Api-Version"),
) -> Dict[str, str]:
    return {"software_id": software_id, "content_api_version": content_api_version}


def error_response(code: str, description: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=[{"codigo": code, "descripcion": description}],
        headers={"Content-Api-Version": API_VERSION},
    )
