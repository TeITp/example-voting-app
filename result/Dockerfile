FROM node:24-bookworm-slim AS base
WORKDIR /usr/local/app
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force && mv node_modules /node_modules
ENV PORT=8080
EXPOSE 8080

FROM base AS dev
COPY --chown=node:node . .
USER node
CMD ["node", "--watch", "server.js"]

FROM base AS final
COPY --chown=node:node . .
USER node
CMD ["node", "server.js"]
