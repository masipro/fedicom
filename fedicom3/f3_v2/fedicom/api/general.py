
from typing import List, Dict

from fastapi import APIRouter, Depends, Response

from config import API_VERSION
from fedicom.schemas.versions import EndpointVersion
from fedicom.models import User
from fedicom.auth_utils import get_current_user
from fedicom.api.deps import common_headers

router = APIRouter(tags=["General"])


@router.get(
    "/endpoint-fedicom-protocol-versions",
    response_model=List[EndpointVersion],
)
def get_endpoint_versions(
    current_user: User = Depends(get_current_user),
    headers: Dict[str, str] = Depends(common_headers),
    response: Response = None,
) -> List[EndpointVersion]:
    if response is not None:
        response.headers["Content-Api-Version"] = API_VERSION

    endpoints = [
        EndpointVersion(
            url="/authenticate",
            method="POST",
            description="Autenticación",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/endpoint-fedicom-protocol-versions",
            method="GET",
            description="Consulta versiones del protocolo",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos",
            method="POST",
            description="Creación de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos/{numeroPedido}",
            method="GET",
            description="Consulta de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/pedidos/{numeroPedido}",
            method="PUT",
            description="Modificación de un pedido",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/devoluciones",
            method="POST",
            description="Creación de devoluciones",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/devoluciones/{numeroDevolucion}",
            method="GET",
            description="Consulta de una devolución",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/facturas",
            method="GET",
            description="Consulta de facturas",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/facturas/{numeroFactura}",
            method="GET",
            description="Obtención de una factura",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes",
            method="GET",
            description="Consulta de albaranes",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes/{numeroAlbaran}",
            method="GET",
            description="Obtención de un albarán",
            version=API_VERSION,
        ),
        EndpointVersion(
            url="/albaranes/confirmacion",
            method="POST",
            description="Confirmación de recepción de albarán",
            version=API_VERSION,
        ),
    ]
    return endpoints
