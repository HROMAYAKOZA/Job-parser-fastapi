FROM node:14

WORKDIR /app

COPY package.json /app

RUN npm install

COPY pages /app/pages
COPY favicon.ico server.js /app/
# COPY favicon.ico /app

EXPOSE 3000

CMD ["node", "server.js"]