# 构建上下文为仓库根目录（docker-compose 中配置）
FROM node:22-alpine AS build
WORKDIR /app
ARG LEETPATH_VERSION=dev
ENV LEETPATH_VERSION=$LEETPATH_VERSION
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
