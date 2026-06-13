FROM node:22-bookworm-slim AS dev

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9.15.2 --activate

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

COPY . .

EXPOSE 5173

CMD ["pnpm", "dev", "--host", "0.0.0.0"]

FROM node:22-bookworm-slim AS builder

WORKDIR /app

ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN corepack enable && corepack prepare pnpm@9.15.2 --activate

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

COPY . .
# Log build-time API URL so deploy logs confirm the production bundle target.
RUN echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" && test -n "${VITE_API_BASE_URL}"
RUN pnpm build

FROM nginx:alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
