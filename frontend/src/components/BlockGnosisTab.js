import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { triggerAgent } from '../services/api';

const TabContainer = styled.div`
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
`;

const Form = styled.div`
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
  &:hover {
    background: #0056b3;
  }
`;

function BlockgnosisTab({ data }) {
  const [taskInput, setTaskInput] = useState('');
  const [taskId, setTaskId] = useState('');
  const [taskResult, setTaskResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchContractData = async () => {
      try {
        const response = await triggerAgent('blockchain_token', {
          task: 'get_task',
          task_id: 'mock_task_id'
        });
        setTaskResult(response.result);
        setError(null);
      } catch (e) {
        setError('Failed to fetch contract data');
        console.error(e);
      }
    };
    fetchContractData();
  }, []);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      const response = await triggerAgent('blockchain_token', {
        task: 'create_task',
        agent_address: '0x' + '0' * 40,
        input: taskInput,
        task_id: `task_${Date.now()}`
      });
      setTaskResult(response.result);
      setTaskInput('');
      setError(null);
    } catch (e) {
      setError('Failed to create task');
      console.error(e);
    }
  };

  const handleGetTask = async (e) => {
    e.preventDefault();
    try {
      const response = await triggerAgent('blockchain_token', {
        task: 'get_task',
        task_id: taskId
      });
      setTaskResult(response.result);
      setError(null);
    } catch (e) {
      setError('Failed to get task');
      console.error(e);
    }
  };

  return (
    <TabContainer>
      <h2>Blockgnosis Platform</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <Form>
        <Input
          type="text"
          placeholder="Task Input"
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
        />
        <Button onClick={handleCreateTask}>Create Task</Button>
      </Form>
      <Form>
        <Input
          type="text"
          placeholder="Task ID"
          value={taskId}
          onChange={(e) => setTaskId(e.target.value)}
        />
        <Button onClick={handleGetTask}>Get Task Result</Button>
      </Form>
      {taskResult && (
        <div>
          <h3>Task Data</h3>
          <pre>{JSON.stringify(taskResult, null, 2)}</pre>
        </div>
      )}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default BlockgnosisTab;