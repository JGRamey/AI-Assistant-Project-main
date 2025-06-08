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

function YouTubeTab({ data }) {
  const [channelId, setChannelId] = useState('');
  const [keywords, setKeywords] = useState('');
  const [result, setResult] = useState(null);
  const [task, setTask] = useState('analytics');

  const handleSubmit = async (e) => {
    e.preventDefault();
    let payload = {};
    if (task === 'analytics') {
      payload = { task: 'fetch_analytics', channel_id: channelId };
    } else if (task === 'schedule') {
      payload = { task: 'fetch_schedule' };
    } else if (task === 'ideas') {
      payload = { task: 'generate_ideas', keywords };
    }
    const response = await triggerAgent('youtube_analytics', payload);
    setResult(response.result);
  };

  return (
    <TabContainer>
      <h2>YouTube</h2>
      <select onChange={(e) => setTask(e.target.value)} value={task}>
        <option value="analytics">Analytics</option>
        <option value="schedule">Video Schedule</option>
        <option value="ideas">Video Ideas</option>
      </select>
      <Form onSubmit={handleSubmit}>
        {task === 'analytics' && (
          <Input
            type="text"
            placeholder="Channel ID"
            value={channelId}
            onChange={(e) => setChannelId(e.target.value)}
          />
        )}
        {task === 'ideas' && (
          <Input
            type="text"
            placeholder="Keywords (e.g., blockchain)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
        )}
        <Button type="submit">Execute</Button>
      </Form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default YouTubeTab;