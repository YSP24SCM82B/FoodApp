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

    // Function to parse bot responses into separate messages, including images
    const parseBotResponse = (text) => {
        // Split the response by line breaks
        const lines = text.split('\n');
        const parsedMessages = [];

        lines.forEach(line => {
            // Check if the line contains an image in Markdown format
            const imageRegex = /!\[Image\]\((.*?)\)/;
            const match = line.match(imageRegex);

            if (match) {
                // Extract the image URL
                const imageUrl = match[1];
                // Remove the image markdown from the line
                const textWithoutImage = line.replace(imageRegex, '').trim();

                // Add the remaining text (if any)
                if (textWithoutImage) {
                    parsedMessages.push({ type: 'bot', text: textWithoutImage });
                }

                // Add the image URL as a separate message
                parsedMessages.push({ type: 'bot', imageUrl });
            } else {
                // Add normal text lines as separate messages
                if (line.trim()) {
                    parsedMessages.push({ type: 'bot', text: line.trim() });
                }
            }
        });

        return parsedMessages;
    };

    // Handle the submit button
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!query.trim()) return;

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
                body: JSON.stringify({ query })  // Send user input to backend
            });

            const data = await res.json();

            // Check if bot response exists and parse it
            if (data.bot_response) {
                const parsedMessages = parseBotResponse(data.bot_response);
                setMessages(prevMessages => [...prevMessages, ...parsedMessages]);
            }

            // Check if food_items exist and is an array
            if (data.food_items && Array.isArray(data.food_items)) {
                // Add food items with images (if available) to the chat
                const foodItems = data.food_items.map(item => ({
                    type: 'bot',
                    text: `${item.name} - ${item.description} (Cuisine: ${item.cuisine}, Price: $${item.price}, Spice Level: ${item.spiceLevel})`,
                    imageUrl: item.imageUrl  // Attach imageUrl if available
                }));

                setMessages(prevMessages => [...prevMessages, ...foodItems]);
            } else if (!data.bot_response) {
                setMessages(prevMessages => [...prevMessages, { type: 'bot', text: 'No recommendations found.' }]);
            }

        } catch (error) {
            console.error("Error fetching bot response:", error);
            setMessages(prevMessages => [...prevMessages, { type: 'bot', text: 'Error fetching response. Please try again.' }]);
        } finally {
            setQuery('');
            setLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((message, index) => (
                    <div key={index} className={`chat-message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}>
                        <div className="message-content">
                            {message.text && <p>{message.text}</p>}
                            {/* Display image if available */}
                            {message.imageUrl && (
                                <img
                                    src={message.imageUrl}
                                    alt="Food item"
                                    className="food-image"
                                />
                            )}
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
                    placeholder="Ask for food recommendations..."
                    className="chat-input"
                    disabled={loading} // Disable input while loading
                />
                <button type="submit" className="send-button" disabled={loading}>Send</button>
            </form>
        </div>
    );
};

export default Chat;
