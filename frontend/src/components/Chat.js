import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';  // Import the Chat component CSS

const Chat = () => {
    const [query, setQuery] = useState('');          // For storing user input
    const [messages, setMessages] = useState([]);    // To store both user and bot messages
    const [loading, setLoading] = useState(false);   // For handling loading state
    const chatWindowRef = useRef(null);  // Ref for the chat window

    // Scroll to the bottom of the chat window when messages are added
    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]);  // This will run every time the messages array is updated

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!query.trim()) return;  // Prevent empty submissions

        // Add user message to chat
        setMessages(prevMessages => [...prevMessages, { type: 'user', text: query }]);
        setLoading(true);  // Start loading

        try {
            // Send POST request to the backend API
            const res = await fetch('http://127.0.0.1:5000/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const data = await res.json();

            // Add bot response to chat
            setMessages(prevMessages => [...prevMessages, { type: 'user', text: query }, { type: 'bot', text: data.bot_response }]);

        } catch (error) {
            console.error("Error fetching bot response:", error);
            // Add error message to chat
            setMessages(prevMessages => [...prevMessages, { type: 'bot', text: 'Error fetching response. Please try again.' }]);
        } finally {
            setQuery('');     // Clear the input field
            setLoading(false); // Stop loading
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((message, index) => (
                    <div key={index} className={`chat-message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}>
                        <div className="message-content">
                            {message.text}
                        </div>
                    </div>
                ))}
                {loading && <div className="bot-message"><div className="message-content">Bot is typing...</div></div>}
            </div>
            <form onSubmit={handleSubmit} className="chat-input-container">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask something..."
                    className="chat-input"
                    disabled={loading} // Disable input while loading
                />
                <button type="submit" className="send-button" disabled={loading}>Send</button>
            </form>
        </div>
    );
};

export default Chat;
