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

const Select = styled.select`
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

function FinancialPlanningTab({ data }) {
  const [task, setTask] = useState('create_budget');
  const [income, setIncome] = useState('');
  const [expenses, setExpenses] = useState('');
  const [age, setAge] = useState('');
  const [retirementAge, setRetirementAge] = useState('');
  const [annualIncome, setAnnualIncome] = useState('');
  const [savingsRate, setSavingsRate] = useState('');
  const [riskTolerance, setRiskTolerance] = useState('moderate');
  const [investmentHorizon, setInvestmentHorizon] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    let payload = { task };
    if (task === 'create_budget') {
      payload = {
        task,
        income: parseFloat(income),
        expenses: JSON.parse(expenses || '[]')
      };
    } else if (task === 'create_retirement_plan') {
      payload = {
        task,
        age: parseInt(age),
        retirement_age: parseInt(retirementAge),
        annual_income: parseFloat(annualIncome),
        savings_rate: parseFloat(savingsRate)
      };
    } else if (task === 'investment_strategy') {
      payload = {
        task,
        risk_tolerance: riskTolerance,
        investment_horizon: parseInt(investmentHorizon)
      };
    }
    const response = await triggerAgent('financial_plan', payload);
    setResult(response.result);
  };

  return (
    <TabContainer>
      <h2>Financial Planning</h2>
      <Select value={task} onChange={(e) => setTask(e.target.value)}>
        <option value="create_budget">Create Budget</option>
        <option value="create_retirement_plan">Retirement Plan</option>
        <option value="investment_strategy">Investment Strategy</option>
      </Select>
      <Form onSubmit={handleSubmit}>
        {task === 'create_budget' && (
          <>
            <Input
              type="number"
              placeholder="Monthly Income"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
            />
            <Input
              type="text"
              placeholder='Expenses (e.g., [{"amount": 1000}])'
              value={expenses}
              onChange={(e) => setExpenses(e.target.value)}
            />
          </>
        )}
        {task === 'create_retirement_plan' && (
          <>
            <Input
              type="number"
              placeholder="Current Age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
            />
            <Input
              type="number"
              placeholder="Retirement Age"
              value={retirementAge}
              onChange={(e) => setRetirementAge(e.target.value)}
            />
            <Input
              type="number"
              placeholder="Annual Income"
              value={annualIncome}
              onChange={(e) => setAnnualIncome(e.target.value)}
            />
            <Input
              type="number"
              placeholder="Savings Rate (e.g., 0.15 for 15%)"
              value={savingsRate}
              onChange={(e) => setSavingsRate(e.target.value)}
            />
          </>
        )}
        {task === 'investment_strategy' && (
          <>
            <Select
              value={riskTolerance}
              onChange={(e) => setRiskTolerance(e.target.value)}
            >
              <option value="conservative">Conservative</option>
              <option value="moderate">Moderate</option>
              <option value="aggressive">Aggressive</option>
            </Select>
            <Input
              type="number"
              placeholder="Investment Horizon (years)"
              value={investmentHorizon}
              onChange={(e) => setInvestmentHorizon(e.target.value)}
            />
          </>
        )}
        <Button type="submit">Execute</Button>
      </Form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default FinancialPlanningTab;