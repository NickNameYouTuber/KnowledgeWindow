import React from 'react';

interface QueryHistoryProps {
  history: { query: string, response: string }[];
}

const QueryHistory: React.FC<QueryHistoryProps> = ({ history }) => {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Query History</h2>
      {history.map((item, index) => (
        <div key={index} className="border p-2 mb-2">
          <div className="font-bold">Query: {item.query}</div>
          <div>Response: {item.response}</div>
        </div>
      ))}
    </div>
  );
};

export default QueryHistory;