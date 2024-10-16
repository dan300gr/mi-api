from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://uvp:Duxg1_400@34.95.154.41:3306/MusicStore"

# Conexión a la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# Configuración del Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================
# MODELOS (SQLAlchemy)
# ===================

# Modelo para la tabla TipoProducto
class TipoProducto(Base):
    __tablename__ = 'TipoProducto'
    tipo_id = Column(Integer, primary_key=True, index=True)
    tipo_nombre = Column(String(40), unique=True, nullable=False)
    tipo_status = Column(String(2), default='A')
    tipo_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla Catalogo
class Catalogo(Base):
    __tablename__ = 'Catalogo'
    catalogo_id = Column(Integer, primary_key=True, index=True)
    catalogo_nombre = Column(String(40))
    catalogo_status = Column(String(2), default='A')
    catalogo_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla Artista
class Artista(Base):
    __tablename__ = 'Artista'
    artista_id = Column(Integer, primary_key=True, index=True)
    artista_nombre = Column(String(40))
    artista_status = Column(String(2), default='A')
    artista_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

# Modelo para la tabla Album
class Album(Base):
    __tablename__ = 'Album'
    album_id = Column(Integer, primary_key=True, index=True)
    album_nombre = Column(String(40))
    artista_id = Column(Integer, ForeignKey('Artista.artista_id'))  # Relación con Artista
    album_status = Column(String(2), default='A')
    album_fecha_modificacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    artista = relationship("Artista", back_populates="albums")  # Relación con Artista
    productos = relationship("Producto", back_populates="album")  # Relación con Producto

# Relación inversa con Artista
Artista.albums = relationship("Album", back_populates="artista")

# Modelo para la tabla Producto
class Producto(Base):
    __tablename__ = 'Producto'
    producto_id = Column(Integer, primary_key=True, index=True)
    producto_nombre = Column(String(40))
    producto_precio = Column(DECIMAL(18, 2))
    tipo_id = Column(Integer, ForeignKey('TipoProducto.tipo_id'))  # Relación con tipo de producto
    catalogo_id = Column(Integer, ForeignKey('Catalogo.catalogo_id'))  # Relación con catálogo
    album_id = Column(Integer, ForeignKey('Album.album_id'))  # Relación con álbum
    producto_status = Column(String(2), default='A')
    producto_fecha_modificacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    album = relationship("Album", back_populates="productos")  # Relación con Álbum
    tipo_producto = relationship("TipoProducto")  # Relación con TipoProducto
    catalogo = relationship("Catalogo")  # Relación con Catalogo
    stocks = relationship("Stock", back_populates="producto")  # Relación con Stock
    inventarios = relationship("Inventario", back_populates="producto")  # Relación con Inventario

# Modelo para la tabla Stock
class Stock(Base):
    __tablename__ = 'Stock'
    stock_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('Producto.producto_id'))  # Relación con Producto
    stock_cantidad = Column(Integer, default=0)
    stock_status = Column(String(2), default='A')
    stock_fecha_modificacion = Column(DateTime)

    # Relaciones
    producto = relationship("Producto", back_populates="stocks")  # Relación inversa con Producto
    inventarios = relationship("Inventario", back_populates="stock")  # Relación con Inventario

# Modelo para la tabla Inventario
class Inventario(Base):
    __tablename__ = 'Inventario'
    inventario_id = Column(Integer, primary_key=True, index=True)
    ubicacion_id = Column(Integer, ForeignKey('Ubicacion.ubicacion_id'))  # Relación con Ubicación
    producto_id = Column(Integer, ForeignKey('Producto.producto_id'))  # Relación con Producto
    stock_id = Column(Integer, ForeignKey('Stock.stock_id'))  # Relación con Stock
    inventario_cantidad = Column(Integer, default=0)
    inventario_status = Column(String(2), default='A')
    inventario_fecha_modificacion = Column(DateTime)

    # Relaciones
    ubicacion = relationship("Ubicacion", back_populates="inventarios")  # Relación con Ubicación
    producto = relationship("Producto", back_populates="inventarios")  # Relación con Producto
    stock = relationship("Stock", back_populates="inventarios")  # Relación con Stock

# Modelo para la tabla Ubicacion
class Ubicacion(Base):
    __tablename__ = 'Ubicacion'
    ubicacion_id = Column(Integer, primary_key=True, index=True)
    ubicacion_nombre = Column(String(40))
    edificio_id = Column(Integer, ForeignKey('Edificio.edificio_id'))  # Relación con Edificio
    ubicacion_status = Column(String(2), default='A')
    ubicacion_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    edificio = relationship("Edificio", back_populates="ubicaciones")  # Relación con Edificio
    inventarios = relationship("Inventario", back_populates="ubicacion")  # Relación con Inventario

# Modelo para la tabla Edificio
class Edificio(Base):
    __tablename__ = 'Edificio'
    edificio_id = Column(Integer, primary_key=True, index=True)
    edificio_nombre = Column(String(40), nullable=False)
    edificio_direccion = Column(String(40), nullable=False)
    edificio_status = Column(String(2), default='A')
    edificio_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    ubicaciones = relationship("Ubicacion", back_populates="edificio")  # Relación con Ubicación

# Modelo para la tabla Proveedor
class Proveedor(Base):
    __tablename__ = 'Proveedor'
    proveedor_id = Column(Integer, primary_key=True, index=True)
    proveedor_nombre = Column(String(40))
    proveedor_direccion = Column(String(40))
    proveedor_telefono = Column(String(40))
    proveedor_correo = Column(String(40))
    proveedor_status = Column(String(2), default='A')
    proveedor_fecha_modificacion = Column(DateTime, default=datetime.utcnow)

# ==================================================
#                   ESQUEMAS
# ==================================================

# Esquemas de Pydantic para Producto
class ProductoCreate(BaseModel):
    producto_id: int
    producto_nombre: str
    producto_precio: float
    catalogo_id: int
    album_id: int
    tipo_id: int  # ID del tipo de producto

class ProductoUpdate(BaseModel):
    producto_nombre: str
    producto_precio: float
    catalogo_id: int
    album_id: int
    tipo_id: int  # Agregado para actualizar el tipo de producto

# Esquemas de Pydantic para Catalogo
class CatalogoCreate(BaseModel):
    catalogo_id: int
    catalogo_nombre: str

class CatalogoUpdate(BaseModel):
    catalogo_nombre: str

# Esquemas de Pydantic para Album
class AlbumCreate(BaseModel):
    album_id: int
    album_nombre: str
    artista_id: int

class AlbumUpdate(BaseModel):
    album_nombre: str
    artista_id: int

# Esquemas de Pydantic para Artista
class ArtistaCreate(BaseModel):
    artista_id: int
    artista_nombre: str

class ArtistaUpdate(BaseModel):
    artista_nombre: str

# Esquemas de Pydantic para TipoProducto
class TipoProductoCreate(BaseModel):
    tipo_id: int  # Corregido a int en lugar de str
    tipo_nombre: str

class TipoProductoUpdate(BaseModel):
    tipo_nombre: str

# Esquemas de Pydantic para Proveedor
class ProveedorCreate(BaseModel):
    proveedor_id: int
    proveedor_nombre: str
    proveedor_direccion: str
    proveedor_telefono: str
    proveedor_correo: str

class ProveedorUpdate(BaseModel):
    proveedor_nombre: str
    proveedor_direccion: str
    proveedor_telefono: str
    proveedor_correo: str

# Esquemas de Pydantic para Edificio
class EdificioCreate(BaseModel):
    edificio_id: int
    edificio_nombre: str
    edificio_direccion: str

class EdificioUpdate(BaseModel):
    edificio_nombre: str
    edificio_direccion: str

# Esquemas de Pydantic para Ubicacion
class UbicacionCreate(BaseModel):
    ubicacion_id: int
    ubicacion_nombre: str
    edificio_id: int

class UbicacionUpdate(BaseModel):
    ubicacion_nombre: str
    edificio_id: int

# Esquemas de Pydantic para Stock
class StockCreate(BaseModel):
    stock_id: int
    producto_id: int
    stock_cantidad: int

class StockUpdate(BaseModel):
    producto_id: int
    stock_cantidad: int

# Esquemas de Pydantic para Inventario
class InventarioCreate(BaseModel):
    inventario_id: int
    ubicacion_id: int
    producto_id: int
    stock_id: int  # Agregado stock_id como llave foránea
    inventario_cantidad: int

class InventarioUpdate(BaseModel):
    ubicacion_id: int
    producto_id: int
    stock_id: int  # Agregado para actualizar el stock asociado
    inventario_cantidad: int
    
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# ===================
# Endpoints para Producto
# ===================
@app.post("/productos/")
def crear_producto(producto: ProductoCreate):
    db = SessionLocal()

    # Verificar si ya existe un producto con el mismo ID
    existing_producto = db.query(Producto).filter(Producto.producto_id == producto.producto_id).first()
    if existing_producto:
        raise HTTPException(status_code=400, detail="Ya existe un producto con el mismo ID.")
    
    db_producto = Producto(**producto.dict(), producto_status='A', producto_fecha_modificacion=datetime.utcnow())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/")
def obtener_productos():
    db = SessionLocal()
    try:
        productos = db.query(Producto).all()  # Obtiene todos los productos sin filtrar por estado
        if not productos:
            raise HTTPException(status_code=404, detail="No hay productos.")
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    db = SessionLocal()
    try:
        producto = db.query(Producto).filter(Producto.producto_id == producto_id).first()
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    db = SessionLocal()
    db_producto = db.query(Producto).filter(Producto.producto_id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db_producto.producto_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.put("/productos/{producto_id}/desactivar")
def desactivar_producto(producto_id: int):
    db = SessionLocal()
    db_producto = db.query(Producto).filter(Producto.producto_id == producto_id).first()
    
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar si el producto está en uso en algún inventario activo
    inventarios_asociados = db.query(Inventario).filter(Inventario.producto_id == producto_id, Inventario.inventario_status == 'A').all()

    # Verificar si el producto está en uso en algún stock activo
    stocks_asociados = db.query(Stock).filter(Stock.producto_id == producto_id, Stock.stock_status == 'A').all()

    # Si el producto está en uso en inventarios activos o en stock activos, bloquear la desactivación
    if inventarios_asociados or stocks_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar el producto porque está asociado a inventarios o stocks activos")

    # Marcar el producto como inactivo
    db_producto.producto_status = 'I'
    db_producto.producto_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Producto desactivado correctamente"}


@app.put("/productos/{producto_id}/activar")
def activar_producto(producto_id: int):
    db = SessionLocal()
    db_producto = db.query(Producto).filter(Producto.producto_id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_producto.producto_status = 'A'  # Cambiar a activo
    db_producto.producto_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Producto activado correctamente"}

# ===================
# Endpoints para Catalogo
# ===================

@app.post("/catalogos/")
def crear_catalogo(catalogo: CatalogoCreate):
    db = SessionLocal()
    
    # Verificar si ya existe un catálogo con el mismo ID
    existing_catalogo = db.query(Catalogo).filter(Catalogo.catalogo_id == catalogo.catalogo_id).first()
    if existing_catalogo:
        raise HTTPException(status_code=400, detail="Ya existe un catálogo con el mismo ID.")
    
    db_catalogo = Catalogo(**catalogo.dict(), catalogo_fecha_modificacion=datetime.utcnow())
    db.add(db_catalogo)
    db.commit()
    db.refresh(db_catalogo)
    return db_catalogo

@app.get("/catalogos/")
def obtener_catalogos():
    db = SessionLocal()
    try:
        catalogos = db.query(Catalogo).all()  # Obtiene todos los catálogos sin filtrar por estado
        if not catalogos:
            raise HTTPException(status_code=404, detail="No hay catálogos disponibles.")
        return catalogos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/catalogos/{catalogo_id}")
def obtener_catalogo(catalogo_id: int):
    db = SessionLocal()
    try:
        catalogo = db.query(Catalogo).filter(Catalogo.catalogo_id == catalogo_id).first()
        if catalogo is None:
            raise HTTPException(status_code=404, detail="Catálogo no encontrado")
        return catalogo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/catalogos/{catalogo_id}")
def actualizar_catalogo(catalogo_id: int, catalogo: CatalogoUpdate):
    db = SessionLocal()
    db_catalogo = db.query(Catalogo).filter(Catalogo.catalogo_id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    db_catalogo.catalogo_nombre = catalogo.catalogo_nombre
    db_catalogo.catalogo_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_catalogo)
    return db_catalogo

@app.put("/catalogos/{catalogo_id}/desactivar")
def desactivar_catalogo(catalogo_id: int):
    db = SessionLocal()

    # Verificar si el catálogo está asociado a productos activos
    productos_asociados = db.query(Producto).filter(Producto.catalogo_id == catalogo_id, Producto.producto_status == 'A').all()
    if productos_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar el catálogo porque está asociado a productos activos.")

    db_catalogo = db.query(Catalogo).filter(Catalogo.catalogo_id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    
    db_catalogo.catalogo_status = 'I'  # Marcar como inactivo
    db_catalogo.catalogo_fecha_modificacion = datetime.utcnow()  # Actualiza la fecha de modificación
    db.commit()
    
    return {"message": "Catálogo desactivado correctamente"}

@app.put("/catalogos/{catalogo_id}/activar")
def activar_catalogo(catalogo_id: int):
    db = SessionLocal()
    db_catalogo = db.query(Catalogo).filter(Catalogo.catalogo_id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    
    db_catalogo.catalogo_status = 'A'  # Cambiar a activo
    db_catalogo.catalogo_fecha_modificacion = datetime.utcnow()  # Actualiza la fecha de modificación
    db.commit()
    
    return {"message": "Catálogo activado correctamente"}

# ===================
# Endpoints para Album
# ===================
@app.post("/albums/")
def crear_album(album: AlbumCreate):
    db = SessionLocal()
    
    # Verificar si ya existe un álbum con el mismo ID
    existing_album = db.query(Album).filter(Album.album_id == album.album_id).first()
    if existing_album:
        raise HTTPException(status_code=400, detail="Ya existe un álbum con el mismo ID.")
    
    db_album = Album(**album.dict(), album_fecha_modificacion=datetime.utcnow())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@app.get("/albums/")
def obtener_albums():
    db = SessionLocal()
    try:
        albums = db.query(Album).all()  # Obtiene todos los álbumes sin filtrar por estado
        if not albums:
            raise HTTPException(status_code=404, detail="No hay álbumes disponibles.")
        return albums
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/albums/{album_id}")
def obtener_album(album_id: int):
    db = SessionLocal()
    try:
        album = db.query(Album).filter(Album.album_id == album_id, Album.album_status == 'A').first()
        if album is None:
            raise HTTPException(status_code=404, detail="Álbum no encontrado")
        return album
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/albums/{album_id}")
def actualizar_album(album_id: int, album: AlbumUpdate):
    db = SessionLocal()
    db_album = db.query(Album).filter(Album.album_id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    db_album.album_nombre = album.album_nombre
    db_album.artista_id = album.artista_id
    db_album.album_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_album)
    return db_album

@app.put("/albums/{album_id}/desactivar")
def desactivar_album(album_id: int):
    db = SessionLocal()
    
    # Verificar si el álbum está en uso en algún producto activo
    productos_asociados = db.query(Producto).filter(Producto.album_id == album_id, Producto.producto_status == 'A').all()
    
    if productos_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar el álbum porque está asociado a productos activos")
    
    db_album = db.query(Album).filter(Album.album_id == album_id).first()
    
    if db_album is None:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    
    db_album.album_status = 'I'
    db_album.album_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Álbum desactivado correctamente"}

@app.put("/albums/{album_id}/activar")
def activar_album(album_id: int):
    db = SessionLocal()
    db_album = db.query(Album).filter(Album.album_id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    db_album.album_status = 'A'
    db_album.album_fecha_modificacion = datetime.utcnow()
    db.commit()
    return {"message": "Álbum activado correctamente"}

# ===================
# Endpoints para Artista
# ===================

@app.post("/artistas/")
def crear_artista(artista: ArtistaCreate):
    db = SessionLocal()

    # Verificar si ya existe un artista con el mismo ID
    existing_artista = db.query(Artista).filter(Artista.artista_id == artista.artista_id).first()
    if existing_artista:
        raise HTTPException(status_code=400, detail="Ya existe un artista con el mismo ID.")
    
    db_artista = Artista(**artista.dict(), artista_fecha_modificacion=datetime.utcnow())
    db.add(db_artista)
    db.commit()
    db.refresh(db_artista)
    return db_artista

@app.get("/artistas/")
def obtener_artistas():
    db = SessionLocal()
    try:
        artistas = db.query(Artista).all()  # Retorna todos los artistas
        if not artistas:
            raise HTTPException(status_code=404, detail="No hay artistas disponibles.")
        return artistas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/artistas/{artista_id}")
def obtener_artista(artista_id: int):
    db = SessionLocal()
    try:
        artista = db.query(Artista).filter(Artista.artista_id == artista_id, Artista.artista_status == 'A').first()
        if artista is None:
            raise HTTPException(status_code=404, detail="Artista no encontrado")
        return artista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/artistas/{artista_id}")
def actualizar_artista(artista_id: int, artista: ArtistaUpdate):
    db = SessionLocal()
    db_artista = db.query(Artista).filter(Artista.artista_id == artista_id).first()
    if db_artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    db_artista.artista_nombre = artista.artista_nombre
    db_artista.artista_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_artista)
    return db_artista

@app.put("/artistas/{artista_id}/desactivar")
def desactivar_artista(artista_id: int):
    db = SessionLocal()

    # Verificar si el artista está en uso en algún producto activo a través de álbumes
    # Obtener los álbumes del artista
    albums_asociados = db.query(Album).filter(Album.artista_id == artista_id).all()

    # Verificar si hay productos activos asociados a esos álbumes
    if albums_asociados:
        album_ids = [album.album_id for album in albums_asociados]
        productos_asociados = db.query(Producto).filter(Producto.album_id.in_(album_ids), Producto.producto_status == 'A').all()
        
        if productos_asociados:
            raise HTTPException(status_code=400, detail="No se puede desactivar el artista porque está asociado a un álbum activo.")
    
    db_artista = db.query(Artista).filter(Artista.artista_id == artista_id).first()
    if db_artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    
    db_artista.artista_status = 'I'  # Marcar como inactivo
    db_artista.artista_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Artista marcado como inactivo"}


@app.put("/artistas/{artista_id}/activar")
def activar_artista(artista_id: int):
    db = SessionLocal()
    db_artista = db.query(Artista).filter(Artista.artista_id == artista_id).first()
    if db_artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    
    db_artista.artista_status = 'A'
    db_artista.artista_fecha_modificacion = datetime.utcnow()
    db.commit()
    return {"message": "Artista activado correctamente"}

# ===================
# Endpoints para TipoProducto
# ===================
@app.post("/tipoproductos/")
def crear_tipo_producto(tipo: TipoProductoCreate):
    db = SessionLocal()
    
    # Verificar si ya existe un tipo de producto con el mismo ID
    existing_tipo = db.query(TipoProducto).filter(TipoProducto.tipo_id == tipo.tipo_id).first()
    if existing_tipo:
        raise HTTPException(status_code=400, detail="Ya existe un tipo de producto con el mismo ID.")
    
    db_tipo = TipoProducto(**tipo.dict(), tipo_fecha_modificacion=datetime.utcnow())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@app.get("/tipoproductos/")
def obtener_tipos_productos():
    db = SessionLocal()
    try:
        tipos_productos = db.query(TipoProducto).all()  # Obtiene todos los tipos sin filtrar por estado
        if not tipos_productos:
            raise HTTPException(status_code=404, detail="No hay tipos de productos disponibles.")
        return tipos_productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tipoproductos/{tipo_id}")
def obtener_tipo_producto(tipo_id: int):
    db = SessionLocal()
    try:
        tipo_producto = db.query(TipoProducto).filter(TipoProducto.tipo_id == tipo_id, TipoProducto.tipo_status == 'A').first()
        if tipo_producto is None:
            raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
        return tipo_producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tipoproductos/{tipo_id}")
def actualizar_tipo_producto(tipo_id: int, tipo: TipoProductoUpdate):
    db = SessionLocal()
    db_tipo_producto = db.query(TipoProducto).filter(TipoProducto.tipo_id == tipo_id).first()
    if db_tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    db_tipo_producto.tipo_nombre = tipo.tipo_nombre
    db_tipo_producto.tipo_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_tipo_producto)
    return db_tipo_producto

@app.put("/tipoproductos/{tipo_id}/desactivar")
def desactivar_tipo_producto(tipo_id: int):
    db = SessionLocal()
    
    # Verificar si el tipo de producto está en uso en algún producto activo
    productos_asociados = db.query(Producto).filter(Producto.tipo_id == tipo_id, Producto.producto_status == 'A').all()
    
    if productos_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar el tipo de producto porque está asociado a productos activos.")
    
    db_tipo_producto = db.query(TipoProducto).filter(TipoProducto.tipo_id == tipo_id).first()
    
    if db_tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    
    db_tipo_producto.tipo_status = 'I'
    db_tipo_producto.tipo_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Tipo de producto desactivado correctamente"}

@app.put("/tipoproductos/{tipo_id}/activar")
def activar_tipo_producto(tipo_id: int):
    db = SessionLocal()
    db_tipo_producto = db.query(TipoProducto).filter(TipoProducto.tipo_id == tipo_id).first()
    if db_tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    db_tipo_producto.tipo_status = 'A'
    db_tipo_producto.tipo_fecha_modificacion = datetime.utcnow()
    db.commit()
    return {"message": "Tipo de producto activado correctamente"}

# ===================
# Endpoints para Proveedor
# ===================
@app.post("/proveedores/")
def crear_proveedor(proveedor: ProveedorCreate):
    db = SessionLocal()

    # Verificar si ya existe un proveedor con el mismo ID
    existing_proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor.proveedor_id).first()
    if existing_proveedor:
        raise HTTPException(status_code=400, detail="Ya existe un proveedor con el mismo ID.")
    
    db_proveedor = Proveedor(**proveedor.dict(), proveedor_fecha_modificacion=datetime.utcnow())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@app.get("/proveedores/")
def obtener_proveedores():
    db = SessionLocal()
    try:
        proveedores = db.query(Proveedor).all()
        if not proveedores:
            raise HTTPException(status_code=404, detail="No hay proveedores.")
        return proveedores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/proveedores/{proveedor_id}")
def obtener_proveedor(proveedor_id: int):
    db = SessionLocal()
    try:
        proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
        if proveedor is None:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return proveedor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/proveedores/{proveedor_id}")
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorUpdate):
    db = SessionLocal()
    db_proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    for key, value in proveedor.dict().items():
        setattr(db_proveedor, key, value)
    
    db_proveedor.proveedor_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@app.put("/proveedores/{proveedor_id}/desactivar")
def desactivar_proveedor(proveedor_id: int):
    db = SessionLocal()
    db_proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    db_proveedor.proveedor_status = 'I'  # Marcar como inactivo
    db_proveedor.proveedor_fecha_modificacion = datetime.utcnow()
    db.commit()
    return {"message": "Proveedor desactivado correctamente"}

@app.put("/proveedores/{proveedor_id}/activar")
def activar_proveedor(proveedor_id: int):
    db = SessionLocal()
    db_proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    db_proveedor.proveedor_status = 'A'  # Cambiar a activo
    db_proveedor.proveedor_fecha_modificacion = datetime.utcnow()
    db.commit()
    return {"message": "Proveedor activado correctamente"}

# ===================
# Endpoints para Edificio
# ===================

@app.post("/edificios/")
def crear_edificio(edificio: EdificioCreate):
    db = SessionLocal()

    # Verificar si ya existe un edificio con el mismo ID
    existing_edificio = db.query(Edificio).filter(Edificio.edificio_id == edificio.edificio_id).first()
    if existing_edificio:
        raise HTTPException(status_code=400, detail="Ya existe un edificio con el mismo ID.")

    db_edificio = Edificio(**edificio.dict(), edificio_fecha_modificacion=datetime.utcnow())
    db.add(db_edificio)
    db.commit()
    db.refresh(db_edificio)
    return db_edificio

@app.get("/edificios/")
def obtener_edificios():
    db = SessionLocal()
    try:
        edificios = db.query(Edificio).all()  # Obtiene todos los edificios
        if not edificios:
            raise HTTPException(status_code=404, detail="No hay edificios disponibles.")
        return edificios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/edificios/{edificio_id}")
def obtener_edificio(edificio_id: int):
    db = SessionLocal()
    try:
        edificio = db.query(Edificio).filter(Edificio.edificio_id == edificio_id).first()
        if edificio is None:
            raise HTTPException(status_code=404, detail="Edificio no encontrado.")
        return edificio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/edificios/{edificio_id}")
def actualizar_edificio(edificio_id: int, edificio: EdificioUpdate):
    db = SessionLocal()
    db_edificio = db.query(Edificio).filter(Edificio.edificio_id == edificio_id).first()
    if db_edificio is None:
        raise HTTPException(status_code=404, detail="Edificio no encontrado.")
    
    for key, value in edificio.dict().items():
        setattr(db_edificio, key, value)
    
    db_edificio.edificio_fecha_modificacion = datetime.utcnow()
    db.commit()
    db.refresh(db_edificio)
    return db_edificio


@app.put("/edificios/{edificio_id}/desactivar")
def desactivar_edificio(edificio_id: int):
    db = SessionLocal()
    
    # Verificar si el edificio está en uso en alguna ubicación activa
    ubicaciones_asociadas = db.query(Ubicacion).filter(Ubicacion.edificio_id == edificio_id, Ubicacion.ubicacion_status == 'A').all()
    
    if ubicaciones_asociadas:
        raise HTTPException(status_code=400, detail="No se puede desactivar el edificio porque está asociado a ubicaciones activas")
    
    db_edificio = db.query(Edificio).filter(Edificio.edificio_id == edificio_id).first()
    
    if db_edificio is None:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    
    db_edificio.edificio_status = 'I'  # Marcar como inactivo
    db_edificio.edificio_fecha_modificacion = datetime.utcnow()  # Actualiza la fecha de modificación
    db.commit()
    
    return {"message": "Edificio desactivado correctamente"}



@app.put("/edificios/{edificio_id}/activar")
def activar_edificio(edificio_id: int):
    db = SessionLocal()
    db_edificio = db.query(Edificio).filter(Edificio.edificio_id == edificio_id).first()
    if db_edificio is None:
        raise HTTPException(status_code=404, detail="Edificio no encontrado.")
    
    db_edificio.edificio_status = 'A'  # Marcar como activo
    db_edificio.edificio_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Edificio activado correctamente"}

#================================
# ENDPOINTS UBICACIONES
#=================================

@app.post("/ubicaciones/")
def crear_ubicacion(ubicacion: UbicacionCreate):
    db = SessionLocal()
    
    # Verificar si ya existe una ubicación con el mismo ID
    existing_ubicacion = db.query(Ubicacion).filter(Ubicacion.ubicacion_id == ubicacion.ubicacion_id).first()
    if existing_ubicacion:
        raise HTTPException(status_code=400, detail="Ya existe una ubicación con el mismo ID.")
    
    db_ubicacion = Ubicacion(**ubicacion.dict(), ubicacion_status='A', ubicacion_fecha_modificacion=datetime.utcnow())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@app.get("/ubicaciones/")
def obtener_ubicaciones():
    db = SessionLocal()
    try:
        ubicaciones = db.query(Ubicacion).all()  # Obtiene todas las ubicaciones sin filtrar por estado
        if not ubicaciones:
            raise HTTPException(status_code=404, detail="No hay ubicaciones.")
        return ubicaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/ubicaciones/{ubicacion_id}")
def obtener_ubicacion(ubicacion_id: int):
    db = SessionLocal()
    try:
        ubicacion = db.query(Ubicacion).filter(Ubicacion.ubicacion_id == ubicacion_id).first()
        if ubicacion is None:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")
        return ubicacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/ubicaciones/{ubicacion_id}")
def actualizar_ubicacion(ubicacion_id: int, ubicacion: UbicacionUpdate):
    db = SessionLocal()
    db_ubicacion = db.query(Ubicacion).filter(Ubicacion.ubicacion_id == ubicacion_id).first()
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    for key, value in ubicacion.dict().items():
        setattr(db_ubicacion, key, value)
    
    db_ubicacion.ubicacion_fecha_modificacion = datetime.utcnow()  # Actualiza la fecha de modificación
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@app.put("/ubicaciones/{ubicacion_id}/desactivar")
def desactivar_ubicacion(ubicacion_id: int):
    db = SessionLocal()
    db_ubicacion = db.query(Ubicacion).filter(Ubicacion.ubicacion_id == ubicacion_id).first()
    
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    # Verificar si la ubicación está en uso en algún inventario activo
    inventarios_asociados = db.query(Inventario).filter(Inventario.ubicacion_id == ubicacion_id, Inventario.inventario_status == 'A').all()

    if inventarios_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar la ubicación porque está asociada a inventarios activos")

    db_ubicacion.ubicacion_status = 'I'  # Marcar como inactiva
    db_ubicacion.ubicacion_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Ubicación desactivada correctamente"}


@app.put("/ubicaciones/{ubicacion_id}/activar")
def activar_ubicacion(ubicacion_id: int):
    db = SessionLocal()
    db_ubicacion = db.query(Ubicacion).filter(Ubicacion.ubicacion_id == ubicacion_id).first()
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    db_ubicacion.ubicacion_status = 'A'  # Cambiar a activa
    db_ubicacion.ubicacion_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Ubicación activada correctamente"}

# ===================
# Endpoints para Inventario
# ===================
@app.post("/inventarios/")
def crear_inventario(inventario: InventarioCreate):
    db = SessionLocal()

    # Verificar si ya existe un inventario con el mismo ID
    existing_inventario = db.query(Inventario).filter(Inventario.inventario_id == inventario.inventario_id).first()
    if existing_inventario:
        raise HTTPException(status_code=400, detail="Ya existe un inventario con el mismo ID.")
    
    db_inventario = Inventario(**inventario.dict(), inventario_fecha_modificacion=datetime.utcnow())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@app.get("/inventarios/")
def obtener_inventarios():
    db = SessionLocal()
    try:
        inventarios = db.query(Inventario).all()  # Obtiene todos los inventarios
        if not inventarios:
            raise HTTPException(status_code=404, detail="No hay inventarios disponibles.")
        return inventarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inventarios/{inventario_id}")
def obtener_inventario(inventario_id: int):
    db = SessionLocal()
    try:
        inventario = db.query(Inventario).filter(Inventario.inventario_id == inventario_id).first()
        if inventario is None:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")
        return inventario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/inventarios/{inventario_id}")
def actualizar_inventario(inventario_id: int, inventario: InventarioUpdate):
    db = SessionLocal()
    db_inventario = db.query(Inventario).filter(Inventario.inventario_id == inventario_id).first()
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    # Actualiza los campos
    db_inventario.ubicacion_id = inventario.ubicacion_id
    db_inventario.producto_id = inventario.producto_id
    db_inventario.stock_id = inventario.stock_id  # Agregado para actualizar stock_id
    db_inventario.inventario_cantidad = inventario.inventario_cantidad
    db_inventario.inventario_fecha_modificacion = datetime.utcnow()

    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@app.put("/inventarios/{inventario_id}/desactivar")
def desactivar_inventario(inventario_id: int):
    db = SessionLocal()
    db_inventario = db.query(Inventario).filter(Inventario.inventario_id == inventario_id).first()
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    db_inventario.inventario_status = 'I'  # Marcar como inactivo
    db_inventario.inventario_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Inventario desactivado correctamente"}

@app.put("/inventarios/{inventario_id}/activar")
def activar_inventario(inventario_id: int):
    db = SessionLocal()
    db_inventario = db.query(Inventario).filter(Inventario.inventario_id == inventario_id).first()
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    db_inventario.inventario_status = 'A'  # Cambiar a activo
    db_inventario.inventario_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Inventario activado correctamente"}


# ===================
# Endpoints para Stock
# ===================
@app.post("/stocks/")
def crear_stock(stock: StockCreate):
    db = SessionLocal()
    
    # Verificar si ya existe un stock con el mismo ID
    existing_stock = db.query(Stock).filter(Stock.stock_id == stock.stock_id).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail="Ya existe un stock con el mismo ID.")
    
    db_stock = Stock(**stock.dict(), stock_fecha_modificacion=datetime.utcnow())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@app.get("/stocks/")
def obtener_stocks():
    db = SessionLocal()
    try:
        stocks = db.query(Stock).all()  # Obtiene todos los stocks
        if not stocks:
            raise HTTPException(status_code=404, detail="No hay stocks disponibles.")
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stocks/{stock_id}")
def obtener_stock(stock_id: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(Stock.stock_id == stock_id).first()
        if stock is None:
            raise HTTPException(status_code=404, detail="Stock no encontrado")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/stocks/{stock_id}")
def actualizar_stock(stock_id: int, stock: StockUpdate):
    db = SessionLocal()
    db_stock = db.query(Stock).filter(Stock.stock_id == stock_id).first()
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    
    # Actualiza los campos
    db_stock.producto_id = stock.producto_id
    db_stock.stock_cantidad = stock.stock_cantidad
    db_stock.stock_fecha_modificacion = datetime.utcnow()

    db.commit()
    db.refresh(db_stock)
    return db_stock

@app.put("/stocks/{stock_id}/desactivar")
def desactivar_stock(stock_id: int):
    db = SessionLocal()
    db_stock = db.query(Stock).filter(Stock.stock_id == stock_id).first()

    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")

    # Verificar si el stock está en uso en algún inventario activo
    inventarios_asociados = db.query(Inventario).filter(Inventario.stock_id == stock_id, Inventario.inventario_status == 'A').all()

    if inventarios_asociados:
        raise HTTPException(status_code=400, detail="No se puede desactivar el stock porque está asociado a inventarios activos")

    # Marcar el stock como inactivo
    db_stock.stock_status = 'I'
    db_stock.stock_fecha_modificacion = datetime.utcnow()
    db.commit()

    return {"message": "Stock desactivado correctamente"}


@app.put("/stocks/{stock_id}/activar")
def activar_stock(stock_id: int):
    db = SessionLocal()
    db_stock = db.query(Stock).filter(Stock.stock_id == stock_id).first()
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    
    db_stock.stock_status = 'A'  # Cambiar a activo
    db_stock.stock_fecha_modificacion = datetime.utcnow()
    db.commit()
    
    return {"message": "Stock activado correctamente"}
