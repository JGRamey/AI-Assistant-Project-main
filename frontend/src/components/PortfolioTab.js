import React, { useState } from 'react';
import styled from 'styled-components';
import { triggerAgent } from '../services/api';

const TabContainer = styled.div`
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const Input = styled.input`
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: #3c3c3c;
  color: #fff;
`;

const Button = styled.button`
  padding: 10px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

function PortfolioTab({ data }) {
  const [assets, setAssets] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await triggerAgent('portfolio', {
      task: 'analyze',
      assets: JSON.parse(assets || '[]')
    });
    setResult(response.result);
  };

  return (
    <TabContainer>
      <h2>Portfolio Management</h2>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          placeholder='Assets (e.g., [{"name": "BTC", "value": 1000}])'
          value={assets}
          onChange={(e) => setAssets(e.target.value)}
        />
        <Button type="submit">Analyze Portfolio</Button>
      </Form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default PortfolioTab;