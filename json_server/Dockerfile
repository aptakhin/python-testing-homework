FROM node:14.15-slim

RUN mkdir /app
WORKDIR /app

ENV JSON_SERVER_VERSION=0.16.3

RUN npm install -g json-server@${JSON_SERVER_VERSION}
COPY package.json package-lock.json ./
RUN npm ci --only="prod"

EXPOSE 80
CMD [ "json-server", "db.json", "--host", "0.0.0.0", "--port", "80" ]
