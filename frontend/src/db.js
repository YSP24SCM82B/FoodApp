const { MongoClient } = require('mongodb');
const url = 'mongodb://localhost:27017';
const client = new MongoClient(url);
const dbName = 'Foodservices';

async function connect() {
    await client.connect();
    console.log('Connected successfully to MongoDB');
    return client.db(dbName);
}

module.exports = connect;
