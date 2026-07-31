# --- Build stage ---
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

ARG VITE_WS_URL=ws://localhost:8000/ws
ENV VITE_WS_URL=$VITE_WS_URL

RUN npm run build

# --- Serve stage ---
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
