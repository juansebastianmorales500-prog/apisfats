from fastapi import FastAPI
from models import producto
from database import get_connection, crear_tabla

app = FastAPI()

crear_tabla()


@app.get("/")
def inicio():
    return {"mensaje": "api funcionando"}


@app.post("/productos")
def crear_producto(datos: producto):
    conn = get_connection()
    conn.execute(
        "INSERT INTO productos (referencia, nombre, precio_cop, precio_usd, estado) VALUES (?, ?, ?, ?, ?)",
        (datos.referencia, datos.nombre, datos.precio_cop, datos.precio_usd, datos.estado)
    )
    conn.commit()
    conn.close()

    return {"mensaje": "Producto creado exitosamente"}


@app.get("/productos")
def listar_productos():
    conn = get_connection()
    productos = conn.execute(
        "SELECT * FROM productos"
    ).fetchall()
    conn.close()
    return [dict(x) for x in productos]