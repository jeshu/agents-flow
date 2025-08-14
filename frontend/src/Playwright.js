import React, { useState } from 'react';
import axios from 'axios';

function Playwright() {
  const [url, setUrl] = useState('');
  const [actions, setActions] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const parsedActions = JSON.parse(actions);
      const res = await axios.post('/api/test', { url, actions: parsedActions });
      setResult(res.data);
    } catch (error) {
      console.error("Error running playwright test", error);
      setResult({ error: error.message });
    }
  };

  return (
    <div>
      <h2>Playwright Test</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
        />
        <textarea
          value={actions}
          onChange={(e) => setActions(e.target.value)}
          placeholder='Enter actions as JSON array'
        />
        <button type="submit">Run Test</button>
      </form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default Playwright;

