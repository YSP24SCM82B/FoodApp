const bcrypt = require('bcrypt');
const connect = require('./db');

// Utility function to hash existing plaintext passwords
async function hashExistingPasswords() {
    const db = await connect();
    const usersCollection = db.collection('Users');
    const users = await usersCollection.find({}).toArray();

    // Loop through users and update passwords if they are in plaintext
    for (let user of users) {
        if (!user.password.startsWith('$2b$')) { // Check if password is already hashed
            const hashedPassword = await bcrypt.hash(user.password, 10);
            await usersCollection.updateOne(
                { _id: user._id },
                { $set: { password: hashedPassword } }
            );
            console.log(`Password updated for user: ${user.username}`);
        }
    }
}

hashExistingPasswords();

// Signup function
async function signup(req, res) {
    const { username, password } = req.body;
    const db = await connect();
    const usersCollection = db.collection('Users');

    // Check if user exists
    const existingUser = await usersCollection.findOne({ username });
    if (existingUser) {
        return res.status(400).json({ message: 'Username already exists' });
    }

    // Hash password and save user
    const hashedPassword = await bcrypt.hash(password, 10);
    await usersCollection.insertOne({ username, password: hashedPassword });
    res.status(201).json({ message: 'User created successfully' });
}

// Login function
async function login(req, res) {
    const { username, password } = req.body;
    const db = await connect();
    const usersCollection = db.collection('Users');

    // Find user and compare password
    const user = await usersCollection.findOne({ username });
    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ message: 'Invalid username or password' });
    }

    res.status(200).json({ message: 'Login successful' });
}

module.exports = { signup, login };
