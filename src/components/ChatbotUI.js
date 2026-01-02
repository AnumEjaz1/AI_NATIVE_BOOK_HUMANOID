import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChatbotUI.module.css';

// API URL configuration for Docusaurus
// Configuration is loaded via client module in docusaurus.config.js
const getAPIBaseUrl = () => {
  // Check if the config is available in the global window object
  if (typeof window !== 'undefined' && window.chatbotConfig && window.chatbotConfig.API_URL) {
    return window.chatbotConfig.API_URL;
  }
  // Default fallback
  return 'http://127.0.0.1:8000';
};

const API_BASE_URL = getAPIBaseUrl();

const ChatbotUI = ({ title = "AI Assistant", initialMessage = "Hello! How can I help you today?" }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: initialMessage, sender: 'bot', timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) {
      return;
    }

    // Add user message to the conversation
    const userMessage = {
      id: Date.now(),
      text: inputValue.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Send request to backend API
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue.trim(),
          user_id: 'current-user', // This could be dynamic in a real app
          metadata: {}
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to the conversation
      const botMessage = {
        id: Date.now() + 1,
        text: data.response || data.answer || 'I received your query.',
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || data.metadata?.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get response. Please try again.');

      // Add error message to conversation
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={clsx('container', styles.chatContainer)}>
      <div className={styles.chatHeader}>
        <h3>{title}</h3>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              styles.message,
              message.sender === 'user' ? styles.userMessage : styles.botMessage
            )}
          >
            <div className={styles.messageContent}>
              <div className={styles.messageText}>{message.text}</div>
              <div className={styles.messageMeta}>
                <span className={styles.timestamp}>{formatTime(message.timestamp)}</span>
                {message.sender === 'bot' && message.sources && message.sources.length > 0 && (
                  <div className={styles.sources}>
                    <details>
                      <summary>Sources</summary>
                      <ul>
                        {message.sources.map((source, index) => (
                          <li key={index}>{source}</li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={clsx(styles.message, styles.botMessage)}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className={styles.errorBanner}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          className={styles.chatInput}
          disabled={isLoading}
          aria-label="Type your message"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className={clsx(
            styles.chatSubmitButton,
            (!inputValue.trim() || isLoading) && styles.chatSubmitButtonDisabled
          )}
          aria-label="Send message"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatbotUI;