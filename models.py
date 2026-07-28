from pydantic import BaseModel


class producto(BaseModel):
    referencia: str
    nombre: str
    precio_cop: float
    precio_usd: float
    estado: bool