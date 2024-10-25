import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chat from './components/Chat';
import Login from './components/Login';
import Signup from './components/Signup';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
    useEffect(() => {
        localStorage.removeItem('isAuthenticated');
    }, []);

    const backgroundStyle = {
        background: "url('/images/background.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    };

    return (
        <Router>
            <div className="App" style={backgroundStyle}>
                <header className="app-header">
                    <h1>Food App Chatbot</h1>
                    <p className="app-tagline">Delicious Meals, Smart Choices. Let Our Chatbot Guide You!</p>
                </header>
                <Routes>
                    <Route path="/" element={<ProtectedRoute element={Chat} />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/signup" element={<Signup />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;