import React from 'react';
import Chat from './components/Chat';
import './App.css'; // Assuming you will also add some global styles here

function App() {
    return (
        <div className="App">
            {/* Header for the Food App */}
            <header className="app-header">
                <h1>Food App Chatbot</h1>
            </header>

            {/* Chat component */}
            <Chat />
        </div>
    );
}

export default App;

