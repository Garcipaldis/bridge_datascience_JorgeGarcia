# Se descarga un linux mínimo con la versión de python especificada
FROM python:3.8

# Copia todo lo que haya a la misma altura de Dockerfile a una carpeta /app dentro del contenedor
COPY . /app

# Muevo el lugar de trabajo a la carpeta /app
WORKDIR /app

# Instala todas las librerías que aparecen en requirements.txt dentro del contenedor
#RUN pip install -r requirements.txt
# This run 
RUN cat requirements.txt | xargs -n 1 pip install --no-cache-dir

# Puerto de flask
#EXPOSE 6060:6060
# Puerto de streamlit
#EXPOSE 8501:8501

#RUN python3 ./src/api/server.py -x Nombre &
#CMD ["python3","./src/api/server.py", "-x", "Nombre"]
CMD ["streamlit","run", "./src/dashboard/app.py"]
#CMD ["python3","./src/api/server.py"]