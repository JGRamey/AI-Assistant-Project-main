import React from 'react';
import styled from 'styled-components';

const SidebarContainer = styled.div`
  width: 200px;
  background: #2c2c2c;
  padding: 20px;
  height: 100vh;
  position: fixed;
`;

const NavItem = styled.div`
  padding: 10px;
  margin-bottom: 10px;
  background: ${props => props.active ? '#007bff' : 'transparent'};
  color: ${props => props.active ? '#fff' : '#ccc'};
  cursor: pointer;
  border-radius: 5px;
  &:hover {
    background: #007bff;
    color: #fff;
  }
`;

function Sidebar({ setActiveTab, activeTab }) {
  const tabs = [
    { id: 'financial', label: 'Financial Planning' },
    { id: 'portfolio', label: 'Portfolio' },
    { id: 'trading', label: 'Trading' },
    { id: 'journal', label: 'Journal' },
    { id: 'youtube', label: 'YouTube' },
    { id: 'coding', label: 'Coding' },
    { id: 'crm', label: 'CRM' },
    { id: 'blockgnosis', label: 'Blockgnosis' },
    { id: 'revenue', label: 'Revenue' }
  ];

  return (
    <SidebarContainer>
      {tabs.map(tab => (
        <NavItem
          key={tab.id}
          active={activeTab === tab.id}
          onClick={() => setActiveTab(tab.id)}
        >
          {tab.label}
        </NavItem>
      ))}
    </SidebarContainer>
  );
}

export default Sidebar;