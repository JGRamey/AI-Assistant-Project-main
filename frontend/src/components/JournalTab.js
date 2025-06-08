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

const TextArea = styled.textarea`
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: #3c3c3c;
  color: #fff;
  height: 100px;
`;

const Button = styled.button`
  padding: 10px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

function JournalTab({ data }) {
  const [content, setContent] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await triggerAgent('journal', {
      task: 'add_entry',
      content
    });
    setResult(response.result);
  };

  return (
    <TabContainer>
      <h2>Journal</h2>
      <Form onSubmit={handleSubmit}>
        <TextArea
          placeholder="Write your journal entry..."
          value={content
          onChange={(e) => setContent(e.target.value)}
        />
        <Button type="submit">Add Entry</Button>
      </Form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default JournalTab;