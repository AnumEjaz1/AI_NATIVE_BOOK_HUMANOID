import React from 'react';
import Layout from '@theme/Layout';
import ChatbotUI from '@site/src/components/ChatbotUI';

function ChatbotPage() {
  return (
    <Layout title="AI Chatbot" description="Interactive chatbot interface for the RAG system">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset--2">
            <h1>AI Assistant</h1>
            <p>Ask questions about humanoid robotics, AI, and related topics.</p>
            <ChatbotUI
              title="AI Assistant"
              initialMessage="Hello! I'm your AI assistant for humanoid robotics and AI topics. What would you like to know?"
            />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ChatbotPage;