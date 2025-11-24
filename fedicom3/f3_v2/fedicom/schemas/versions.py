
from .common import FedicomBase


class EndpointVersion(FedicomBase):
    url: str
    method: str
    description: str
    version: str
