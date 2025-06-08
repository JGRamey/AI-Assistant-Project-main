import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Sidebar from './Sidebar';
import FinancialPlanningTab from './FinancialPlanningTab';
import PortfolioTab from './PortfolioTab';
import TradingTab from './TradingTab';
import JournalTab from './JournalTab';
import YouTubeTab from './YouTubeTab';
import CodingTab from './CodingTab';
import CRMTab from './CRMTab';
import BlockgnosisTab from './BlockgnosisTab';
import { triggerAgent } from '../services/api';

const DashboardContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #1c1c1c;
  color: #fff;
`;

const Content = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
`;

function Dashboard() {
  const [activeTab, setActiveTab] = useState('financial');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await triggerAgent('dashboard', {
          task: 'view',
          task_ids: ['task1', 'task2']
        });
        setData(response);
        setError(null);
      } catch (e) {
        setError('Failed to load dashboard data');
        console.error(e);
      }
    };
    fetchDashboardData();
  }, []);

  const renderTab = () => {
    switch (activeTab) {
      case 'financial':
        return <FinancialPlanningTab data={data?.financial_data} />;
      case 'portfolio':
        return <PortfolioTab data={data?.portfolio_data} />;
      case 'trading':
        return <TradingTab data={data?.trading_data} />;
      case 'journal':
        return <JournalTab data={data?.journal_data} />;
      case 'youtube':
        return <YouTubeTab data={data?.youtube_data} />;
      case 'coding':
        return <CodingTab data={data?.coding_data} />;
      case 'crm':
        return <CRMTab data={data?.crm_data} />;
      case 'blockgnosis':
        return <BlockgnosisTab data={data?.blockgnosis_data} />;
      case 'revenue':
        return <RevenueTab data={data?.revenue_data} />;
      default:
        return <div>Select a tab</div>;
    }
  };

  return (
    <DashboardContainer>
      <Sidebar setActiveTab={setActiveTab} activeTab={activeTab} />
      <Content>
        {error && <div style={{color: 'red'}}>{error}</div>}
        {renderTab()}
      </Content>
    </DashboardContainer>
  );
}

function RevenueTab({ data }) {
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRevenue = async () => {
      try {
        const response = await triggerAgent('token_manage', { task: 'generate_financial_report' });
        setReport(response.result);
        setError(null);
      } catch (e) {
        setError('Failed to load revenue data');
        console.error(e);
      }
    };
    fetchRevenue();
  }, []);

  return (
    <div>
      <h2>Revenue Overview</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {report && (
        <pre>{JSON.stringify(report, null, 2)}</pre>
      )}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

export default Dashboard;