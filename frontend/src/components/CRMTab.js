import React, { useState, useEffect } from 'react';
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

function CRMTab({ data }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    const fetchContacts = async () => {
      const response = await triggerAgent('crm', { task: 'list_contacts' });
      setContacts(response.result);
    };
    fetchContacts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await triggerAgent('crm', {
      task: 'add_contact',
      contact: { name, email }
    });
    const response = await triggerAgent('crm', { task: 'list_contacts' });
    setContacts(response.result);
    setName('');
    setEmail('');
  };

  return (
    <TabContainer>
      <h2>CRM</h2>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Button type="submit">Add Contact</Button>
      </Form>
      <h3>Contacts</h3>
      <pre>{JSON.stringify(contacts, null, 2)}</pre>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default CRMTab;