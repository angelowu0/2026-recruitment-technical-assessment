FROM node:24.10.0

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .
RUN npx tsc

CMD [ "node", "dist/server.js" ]
