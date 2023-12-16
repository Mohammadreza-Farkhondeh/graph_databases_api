import React, { useState } from 'react';
import { Button, Input, Form } from 'antd';
import api from "../Api";

const Connection = ({ onConnect }) => {
  const [host, setHost] = useState('');
  const [graphname, setGraphname] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [secret, setSecret] = useState('');

  const handleSubmit = async () => {
    await api.post("graph/connect", {host, graphname, username, password, secret})
    onConnect();
  };

  return (
    <div>
      <h2>Connect to Graph</h2>
      <Form layout="vertical">
        <Form.Item label="Host">
          <Input
            type="text"
            value={host}
            onChange={(e) => setHost(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Graph name">
          <Input
            type="text"
            value={graphname}
            onChange={(e) => setGraphname(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="username">
          <Input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Password">
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Secret">
          <Input
            type="text"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            placeholder="not neccessary, api will create secret itself"
          />
        </Form.Item>
        <Button type="primary" onClick={handleSubmit}>
          Connect
        </Button>
      </Form>
    </div>
  );
};

export default Connection;