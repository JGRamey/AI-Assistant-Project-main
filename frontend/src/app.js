import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import styled from 'styled-components';
import { supabase } from './services/api';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #1a1a1a;
  color: #fff;
`;

const Content = styled.div`
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
`;

function App() {
  const [session, setSession] = useState(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
  }, []);

  if (!session) {
    return <Navigate to="/login" />;
  }

  return (
    <Router>
      <AppContainer>
        <Sidebar />
        <Content>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </Content>
      </AppContainer>
    </Router>
  );
}

export default App;