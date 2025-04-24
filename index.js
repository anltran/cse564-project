const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.sendFile('index.html', {root: __dirname })
});

app.get('/data', (req, res) => {
    res.sendFile('data.csv', {root: __dirname })
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});