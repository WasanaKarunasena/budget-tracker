import React, { useState, useEffect } from 'react';
import AddTransaction from './components/AddTransaction';
import TransactionList from './components/TransactionList';
import Summary from './components/Summary';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState({ income: 0, expenses: 0 });

  const fetchTransactions = async () => {
    const response = await axios.get('http://localhost:5000/api/transactions');
    setTransactions(response.data);
  };

  const fetchSummary = async () => {
    const response = await axios.get('http://localhost:5000/api/summary');
    setSummary(response.data);
  };

  useEffect(() => {
    fetchTransactions();
    fetchSummary();
  }, []);

  const addTransaction = async (transaction) => {
    await axios.post('http://localhost:5000/api/transactions', transaction);
    fetchTransactions();
    fetchSummary();
  };

  return (
    <div className="container">
      <h1 className="text-center my-4">Personal Budget Tracker</h1>
      <Summary income={summary.income} expenses={summary.expenses} />
      <AddTransaction onAddTransaction={addTransaction} />
      <TransactionList transactions={transactions} />
    </div>
  );
};

export default App;
