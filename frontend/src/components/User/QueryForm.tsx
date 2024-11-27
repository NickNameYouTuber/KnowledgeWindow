import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface QueryFormProps {
  onHistoryUpdate: (history: { query: string, response: string }[]) => void;
}

const QueryForm: React.FC<QueryFormProps> = ({ onHistoryUpdate }) => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState<{ query: string, response: string }[]>([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:5000/history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setHistory(res.data);
        onHistoryUpdate(res.data);
      } catch (error) {
        console.error("Error fetching history: ", error);
      }
    };

    fetchHistory();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post(`http://127.0.0.1:5000/search?query=${query}`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const newResponse = res.data.response;
      setResponse(newResponse);
      const newHistory = [...history, { query, response: newResponse }];
      setHistory(newHistory);
      onHistoryUpdate(newHistory);
    } catch (error) {
      console.error("Error fetching data: ", error);
    }
  };

  return (
    <div className="mb-4">
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border rounded-xl p-2 w-full"
          placeholder="Enter your query"
        />
        <button type="submit" className="bg-blue-500 rounded-xl text-white p-2">Submit</button>
      </form>
      {response && <div className="border p-2 mt-4">{response}</div>}
    </div>
  );
};

export default QueryForm;