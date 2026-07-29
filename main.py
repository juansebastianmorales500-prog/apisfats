from fastapi import FastAPI
from models import Producto
from database import get_connection, crear_tabla

app = FastAPI()

crear_tabla()


dolar = 3205.87

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}



@app.post("/productos")
def crear_producto(datos: Producto):

    precio_usd = round(datos.precio_cop / dolar, 2)

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO productos
        (referencia, nombre, precio_cop, precio_usd, estado)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datos.referencia,
            datos.nombre,
            datos.precio_cop,
            precio_usd,
            datos.estado
        )
    )

    conn.commit()
    conn.close()

    return {
        "mensaje": "Producto creado",
        "precio_usd": precio_usd
    }



@app.get("/productos")
def listar_productos():

    conn = get_connection()

    productos = conn.execute(
        "SELECT * FROM productos"
    ).fetchall()

    conn.close()

    return [dict(x) for x in productos]



@app.get("/productos/{id}")
def buscar_producto(id: int):

    conn = get_connection()

    producto = conn.execute(
        "SELECT * FROM productos WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if producto:
        return dict(producto)

    return {"mensaje": "Producto no encontrado"}



@app.put("/productos/{id}")
def actualizar_producto(id: int, datos: Producto):

    precio_usd = round(datos.precio_cop / dolar, 2)

    conn = get_connection()

    conn.execute(
        """
        UPDATE productos
        SET referencia=?,
            nombre=?,
            precio_cop=?,
            precio_usd=?,
            estado=?
        WHERE id=?
        """,
        (
            datos.referencia,
            datos.nombre,
            datos.precio_cop,
            precio_usd,
            datos.estado,
            id
        )
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Producto actualizado"}



@app.delete("/productos/{id}")
def eliminar_producto(id: int):

    conn = get_connection()

    conn.execute(
        "DELETE FROM productos WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Producto eliminado"}