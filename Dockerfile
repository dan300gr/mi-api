# Usar una imagen base oficial de Python
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /TiendaMusica

# Copiar el archivo de requisitos
COPY requirements.txt /TiendaMusica/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r /TiendaMusica/requirements.txt

# Copiar el resto del código de la aplicación
COPY . /TiendaMusica/

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]