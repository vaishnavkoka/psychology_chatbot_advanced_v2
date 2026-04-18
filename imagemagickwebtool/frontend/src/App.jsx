import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [mutations, setMutations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch mutations from backend
    const fetchMutations = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/mutations');
        const data = await response.json();
        setMutations(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchMutations();
  }, []);

  if (loading) {
    return (
      <div className="App">
        <div className="container">
          <h1>📸 Image Mutation Tool</h1>
          <div className="loading">Loading mutations...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="container">
          <h1>📸 Image Mutation Tool</h1>
          <div className="error">
            Error: {error}
            <p>Make sure the backend is running on http://localhost:5000</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="container">
        <h1>🎨 Image Mutation Tool</h1>
        
        <div className="status-bar">
          <span className="status-badge success">✅ Backend Connected</span>
          <span className="status-badge">v1.0.0</span>
        </div>

        <div className="info-box">
          <h2>Welcome! 👋</h2>
          <p>The Image Mutation Tool backend is running and responding to API calls.</p>
          <p><strong>Next steps:</strong></p>
          <ol>
            <li>Read <strong>TOOL_DESIGN_PLAN.md</strong> to understand the features</li>
            <li>Follow <strong>DEVELOPER_GUIDE.md</strong> to add backend implementations</li>
            <li>Complete the frontend components in the <strong>components/</strong> folder</li>
          </ol>
        </div>

        <div className="mutations-display">
          <h2>Available Mutations</h2>
          
          <div className="mutations-section">
            <h3>Continuous Mutations (Numeric Parameters)</h3>
            <div className="mutations-grid">
              {mutations?.continuous && Object.entries(mutations.continuous).map(([key, mutation]) => (
                <div key={key} className="mutation-card">
                  <h4>{mutation.name}</h4>
                  <p>{mutation.description}</p>
                  {Object.entries(mutation.parameters).map(([pkey, param]) => (
                    <div key={pkey} className="param-info">
                      <small>{param.type}: {param.min} - {param.max}</small>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          <div className="mutations-section">
            <h3>Discrete Mutations (Fixed Options)</h3>
            <div className="mutations-grid">
              {mutations?.discrete && Object.entries(mutations.discrete).map(([key, mutation]) => (
                <div key={key} className="mutation-card">
                  <h4>{mutation.name}</h4>
                  <p>{mutation.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="api-section">
          <h2>API Endpoints</h2>
          <pre className="code-block">
{`GET  /api/health        - Check server status
GET  /api/mutations     - List all mutations
POST /api/upload        - Upload images
POST /api/mutate        - Apply mutation
GET  /api/download      - Download results
GET  /api/manifest      - Get mutation metadata`}
          </pre>
          <a href="http://localhost:5000/api/mutations" target="_blank" rel="noopener noreferrer" className="btn">
            View API Mutations →
          </a>
        </div>

        <div className="footer">
          <p>📚 See <strong>DOCUMENTATION_INDEX.md</strong> for complete guides</p>
          <p>🚀 Ready to start building? Check <strong>DEVELOPER_GUIDE.md</strong></p>
        </div>
      </div>
    </div>
  );
}

export default App;
