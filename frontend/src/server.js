const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { signup, login } = require('./authController');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post('/signup', signup);
app.post('/login', login);

const PORT = 5001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
