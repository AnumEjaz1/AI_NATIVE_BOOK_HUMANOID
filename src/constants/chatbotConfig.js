// Chatbot configuration constants
// These can be overridden by environment variables during build time

// Default configuration
const defaultConfig = {
  API_URL: 'http://127.0.0.1:8000',
};

// Get configuration from environment or use defaults
const chatbotConfig = {
  API_URL: process.env.REACT_APP_API_URL || defaultConfig.API_URL,
};

// Make the config available globally
if (typeof window !== 'undefined') {
  window.chatbotConfig = window.chatbotConfig || {};
  Object.assign(window.chatbotConfig, chatbotConfig);
}

export default chatbotConfig;