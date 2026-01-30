FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose port của Vite
EXPOSE 5173

# Chạy Vite với flag --host để truy cập được từ bên ngoài container
CMD ["npm", "run", "dev", "--", "--host"]