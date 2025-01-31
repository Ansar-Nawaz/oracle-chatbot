import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const newSessionId = crypto.randomUUID();
    setSessionId(newSessionId);
  }, []);

  const getSuggestions = async (text) => {
    const res = await axios.get(`http://localhost:5000/suggest?q=${text}`);
    setSuggestions(res.data);
  };

  const handleSubmit = async () => {
    const res = await axios.post('http://localhost:5000/ask', {
      session_id: sessionId,
      query: query
    });
    setResponse(res.data.response);
  };

  const rateSolution = async (rating) => {
    await axios.post('http://localhost:5000/feedback', {
      session_id: sessionId,
      query: query,
      response: response,
      rating: rating
    });
  };

  return (
    <div className="App">
      <h1>Oracle Error Assistant</h1>
      <div className="chat-container">
        <div className="suggestion-box">
          {suggestions.map((s, i) => (
            <div key={i} onClick={() => setQuery(s)}>{s}</div>
          ))}
        </div>
        <input
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            getSuggestions(e.target.value);
          }}
          placeholder="Describe your Oracle error..."
        />
        <button onClick={handleSubmit}>Ask</button>
        {response && (
          <div className="response-box">
            <h3>{response.code}</h3>
            <p>{response.description}</p>
            <div className="feedback-buttons">
              <button onClick={() => rateSolution('helpful')}>👍 Helpful</button>
              <button onClick={() => rateSolution('unhelpful')}>👎 Not Helpful</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

