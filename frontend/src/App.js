import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Chat from './Chat';
import Playwright from './Playwright';

function App() {
  const [servers, setServers] = useState([]);

  useEffect(() => {
    axios.get('/api/servers')
      .then(response => {
        setServers(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the servers!", error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>MCP Servers</h1>
        <ul>
          {servers.map(server => (
            <li key={server.id}>
              {server.name} - {server.status}
            </li>
          ))}
        </ul>
        <Chat />
        <Playwright />
      </header>
    </div>
  );
}

export default App;

