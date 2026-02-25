import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, GraduationCap, Loader2, User } from 'lucide-react';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });

            const data = await response.json();
            if (data.status === 'success') {
                setMessages(prev => [...prev, { role: 'teacher', content: data.response }]);
            } else {
                setMessages(prev => [...prev, { role: 'error', content: data.error || 'Oops! Something went wrong.' }]);
            }
        } catch (error) {
            setMessages(prev => [...prev, { role: 'error', content: 'Connection failed. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="header">
                <GraduationCap className="logo-icon" />
                <h1>Prof. Science</h1>
                <p>Your step-by-step guide to the universe!</p>
            </header>

            <div className="chat-window" ref={scrollRef}>
                {messages.length === 0 && (
                    <div className="welcome-message">
                        <GraduationCap size={48} className="placeholder-icon" />
                        <h2>Hello there! I'm Science professor.</h2>
                        <p>Ask me anything about physics, chemistry, biology, or the stars!</p>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div key={index} className={`message-row ${msg.role}`}>
                        <div className="avatar">
                            {msg.role === 'user' ? <User size={20} /> : <GraduationCap size={20} />}
                        </div>
                        <div className="message-content">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="message-row teacher loading">
                        <div className="avatar"><GraduationCap size={20} /></div>
                        <div className="message-content">
                            <div className="typing-indicator">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className="input-area">
                <div className="input-wrapper">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask a science question..."
                        disabled={isLoading}
                    />
                    <button onClick={handleSend} disabled={isLoading || !input.trim()}>
                        {isLoading ? <Loader2 className="spinning" /> : <Send />}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;
