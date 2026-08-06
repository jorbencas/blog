# ── Build stage ──
FROM node:22-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Production stage ──
FROM node:22-alpine AS runner
WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/.vercel/output/static ./dist
COPY --from=builder /app/public ./public

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 4321

CMD ["serve", "dist", "-l", "4321", "--single"]
