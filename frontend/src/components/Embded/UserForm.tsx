import React, { useState } from 'react';
import axios from 'axios';

interface UserFormProps {
  format: 'small' | 'full';
  color: string;
}

const UserForm: React.FC<UserFormProps> = ({ format, color }) => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post(`http://127.0.0.1:5000/search?query=${query}`);
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error fetching data: ", error);
    }
  };

  const formStyle = {
    backgroundColor: color,
    padding: format === 'full' ? '20px' : '10px',
    borderRadius: '5px',
    width: format === 'full' ? '100%' : '300px',
    margin: 'auto',
  };

  return (
    <div style={formStyle}>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 w-full"
          placeholder="Enter your query"
        />
        <button type="submit" className="bg-blue-500 text-white p-2">Submit</button>
      </form>
      {response && <div className="border p-2 mt-4">{response}</div>}
    </div>
  );
};

export default UserForm;