# Quickstart: RAG UI Chatbot Component

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+ with pip (for backend)
- Running FastAPI backend server (port 8000)

## Setup

### 1. Start the Backend Server

First, ensure your FastAPI backend is running:

```bash
cd backend
uvicorn src.rag_agent.api:app --reload --port 8000
```

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Run the Docusaurus Frontend

```bash
npm run start
```

## Environment Configuration

The chatbot component can be configured with a custom API URL using environment variables during build time:

```bash
REACT_APP_API_URL=http://your-backend-url:8000 npm run start
```

Or by setting it in a `.env` file in the root directory:

```
REACT_APP_API_URL=http://your-backend-url:8000
```

## Using the Chatbot Component

### Adding to a Page

The chatbot component can be imported and used in any Docusaurus page:

```jsx
import ChatbotUI from '@site/src/components/ChatbotUI';

function MyPage() {
  return (
    <div>
      <h1>My Page with Chatbot</h1>
      <ChatbotUI
        title="AI Assistant"
        initialMessage="Hello! How can I help you?"
      />
    </div>
  );
}
```

## Component Properties

- `title`: (string) Title displayed in the chat header (default: "AI Assistant")
- `initialMessage`: (string) First message displayed to the user (default: "Hello! How can I help you today?")

## API Integration

The component communicates with the backend via:

- **POST** `/query` - Send user queries to the RAG system
- Request format: `{ query: string, user_id: string, metadata: object }`
- Response format: `{ response: string, sources: array, metadata: object }`

## Troubleshooting

### Common Issues

1. **"process is not defined" Error**: This indicates the environment variables aren't properly configured. The component now uses a client module approach to handle this.
2. **CORS Errors**: Ensure the backend has CORS enabled for your frontend origin
3. **Connection Refused**: Verify the backend server is running on the configured URL
4. **Component Not Found**: Verify the component path is correct in your imports

### Development

To run with a different backend URL during development:

```bash
REACT_APP_API_URL=http://localhost:8000 npm run start
```

## Files Created

- `src/components/ChatbotUI.js` - Main React component
- `src/components/ChatbotUI.module.css` - Component styling
- `src/pages/chatbot.js` - Sample page demonstrating usage
- `src/constants/chatbotConfig.js` - Configuration constants