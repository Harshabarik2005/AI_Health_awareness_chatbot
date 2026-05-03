import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
  HeartPulse, Send, ShieldCheck, User, CheckCircle2, MessageSquare, Info
} from 'lucide-react';
import './index.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const LOADING_STATES = ['Thinking...', 'Analyzing Symptoms...', 'Diagnosing...', 'Validating...', 'Finalizing Diagnosis...'];

function App() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I am here to provide you with verified health information. How can I help you today?',
      disclaimer: false
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isServerLive, setIsServerLive] = useState(false);
  const [loadingTextIndex, setLoadingTextIndex] = useState(0);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (!isLoading) {
      return undefined;
    }

    const interval = setInterval(() => {
      setLoadingTextIndex((prev) => (prev + 1) % LOADING_STATES.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [isLoading]);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/health`);
        setIsServerLive(res.data.status === 'healthy');
      } catch {
        setIsServerLive(false);
      }
    };
    checkHealth();
  }, []);

  const startNewConversation = () => {
    setMessages([
      {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Hello! I am here to provide you with verified health information. How can I help you today?',
        disclaimer: false
      }
    ]);
    setInput('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { id: Date.now().toString(), role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoadingTextIndex(0);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, { query: userMessage.content });
      const data = response.data;
      
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        disclaimer: data.disclaimer
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I am having trouble reaching the server right now. Please try again later.'
      }]);
    } finally {
      setIsLoading(false);
      setLoadingTextIndex(0);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
  };

  return (
    <div className="app-container">
      <div className="ambient-glow"></div>

      {/* Sidebar - Clean, Non-Technical */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="brand-icon">
            <HeartPulse size={24} />
          </div>
          <div>
            <h1 className="brand-title">Health <span className="text-gradient">Assistant</span></h1>
            <p className="brand-subtitle">Verified Information</p>
          </div>
        </div>

        <div className="sidebar-content">
          <div className="info-card clickable" onClick={startNewConversation}>
            <h3><MessageSquare size={16} /> New Conversation</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Ask about symptoms, prevention, and treatments for common diseases.
            </p>
          </div>

          <div className="info-card" style={{ background: 'rgba(16, 185, 129, 0.05)', borderColor: 'rgba(16, 185, 129, 0.2)' }}>
            <h3><CheckCircle2 size={16} color="var(--accent-primary)" /> Trusted Sources</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              All answers are sourced directly from verified World Health Organization (WHO) and CDC guidelines.
            </p>
          </div>

          <div className="info-card">
            <h3><ShieldCheck size={16} /> Secure & Private</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Personal details are automatically removed before AI processing.
            </p>
          </div>

          <div style={{ marginTop: 'auto', paddingTop: '20px' }}>
            <div className="status-indicator">
              <div className={`status-dot ${!isServerLive ? 'error' : ''}`}></div>
              {isServerLive ? 'Online & Ready' : 'Connecting...'}
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="main-content">
        <div className="chat-container">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.role}`}>
              <div className={`avatar ${msg.role}`}>
                {msg.role === 'assistant' ? <HeartPulse size={20} /> : <User size={18} />}
              </div>
              
              <div className="message-content">
                <div className="message-bubble">
                  {msg.role === 'assistant' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>

                {/* Disclaimer attached to AI responses */}
                {msg.role === 'assistant' && msg.disclaimer && (
                  <div style={{ display: 'flex' }}>
                    <div className="disclaimer-box">
                      <Info size={14} style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{msg.disclaimer.replace('⚕️', '').trim()}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message-wrapper assistant">
              <div className="avatar assistant">
                <HeartPulse size={20} />
              </div>
              <div className="message-content">
                <div className="message-bubble" style={{ padding: '12px 16px' }}>
                  <div className="typing-indicator diagnostic-text">
                    <span>{LOADING_STATES[loadingTextIndex]}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="input-container">
          <form className="input-box" onSubmit={handleSubmit}>
            <textarea
              className="input-field"
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              placeholder="Message Health Assistant..."
              rows={1}
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={!input.trim() || isLoading}
            >
              <Send size={18} />
            </button>
          </form>
          <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            This assistant provides general public health information. It does not provide medical advice.
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
