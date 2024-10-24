// import React from 'react';
// import Chat from './components/Chat';
// import './App.css'; // Assuming you will also add some global styles here
//
// function App() {
//     return (
//         <div className="App">
//             {/* Header for the Food App */}
//             <header className="app-header">
//                 <h1>Food App Chatbot</h1>
//             </header>
//             <footer className="app-footer">
//                 <p>&copy; Food App Done by: </p>
//             </footer>
//
//             {/* Chat component */}
//             <Chat/>
//         </div>
//     );
// }
//
// export default App;
//


import React from 'react';
import Chat from './components/Chat';
import './App.css'; // Keep the rest of your CSS styles

function App() {
    const backgroundStyle = {
        backgroundImage: 'url(/images/background.jpg)',  // Use the correct path from the public folder
        backgroundSize: 'cover',
        backgroundPosition: 'center center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        alignItems: 'center',
    };

    return (
        <div className="App" style={backgroundStyle}>
            {/* Header for the Food App */}
            <header className="app-header">
                <h1>Food App Chatbot</h1>
            </header>

            <div className="app-tagline">
                <h3 className="h3">Delicious Meals, Smart Choices. Let Our Chatbot Guide You!</h3>
            </div>

            {/* Chat component */}
            <Chat/>
        </div>
    );
}

export default App;
