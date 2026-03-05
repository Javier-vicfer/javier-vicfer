# Usamos una versión ligera de Node.js
FROM node:18

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de configuración y descargamos las dependencias (Express, etc.)
COPY package.json ./
RUN npm install

# Copiamos el resto de nuestro código
COPY . .

# Exponemos el puerto 3000 (el que pedía el profe)
EXPOSE 3000

# Comando para arrancar el servidor
CMD ["node", "server.js"]