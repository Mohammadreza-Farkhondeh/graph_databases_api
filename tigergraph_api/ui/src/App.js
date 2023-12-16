import React, { useState } from 'react';
import Connection from './components/Connection';
import Dashboard from './components/Dashboard';

function App() {
  const [connected, setConnected] = useState(false );

  const handleConnectionChange = (isConnected) => {
    setConnected(isConnected);
  };

  return (
    <div className="App">
      {connected ? (
        <Dashboard />
      ) : (
        <Connection onConnect={() => handleConnectionChange(false)} />
      )}
    </div>
  );
}

export default App;
