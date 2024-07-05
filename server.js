const express = require('express');
const app = express();
const path = require('path');

const PORT = process.env.PORT || 3000;
const SERV_IP = process.env.SERV_IP || "127.0.0.1";

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'pages', 'index.html'));
});
app.get('/favicon.ico', (req, res) => {
  res.sendFile(path.join(__dirname, 'favicon.ico'));
});

app.use(express.static(path.join(__dirname,"pages")));

app.listen(PORT, () => {
  console.log(`Server is running on http://${SERV_IP}:${PORT}`);
});
