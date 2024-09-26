import React from 'react';

const Summary = ({ income, expenses }) => {
  return (
    <div className="alert alert-info text-center">
      <h4>Monthly Summary</h4>
      <p>Income: ${income}</p>
      <p>Expenses: ${expenses}</p>
      <p>Balance: ${income - expenses}</p>
    </div>
  );
};

export default Summary;
