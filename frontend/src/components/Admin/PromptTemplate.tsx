import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FileText, Edit, Save, X } from 'lucide-react';
import axiosWithAuth from '../../axiosWithAuth';

interface PromptTemplate {
  id: number;
  name: string;
  content: string;
}

const PromptTemplate = () => {
  const [template, setTemplate] = useState<PromptTemplate | null>(null);
  const [editing, setEditing] = useState(false);
  const [editedContent, setEditedContent] = useState('');

  useEffect(() => {
    fetchTemplate();
  }, []);

  const fetchTemplate = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found');
      return;
    }
    const response = await axiosWithAuth(token).get<PromptTemplate>('http://127.0.0.1:5000/prompt-template');
    setTemplate(response.data);
    setEditedContent(response.data.content);
  };

  const handleEdit = () => {
    setEditing(true);
  };

  const handleSave = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found');
      return;
    }
    await axiosWithAuth(token).put(`http://127.0.0.1:5000/prompt-template`, { content: editedContent });
    setEditing(false);
    fetchTemplate();
  };

  const handleCancel = () => {
    setEditing(false);
    setEditedContent(template?.content || '');
  };

  if (!template) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center space-x-2 mb-6">
        <FileText className="h-5 w-5 text-blue-500" />
        <h2 className="text-lg font-semibold">Prompt Template</h2>
      </div>

      <div className="border-b border-gray-200 pb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-md font-medium">{template.name}</h3>
          {editing ? (
            <div className="flex space-x-2">
              <button onClick={handleSave} className="bg-green-500 text-white p-2 rounded">
                <Save className="h-4 w-4" />
              </button>
              <button onClick={handleCancel} className="bg-red-500 text-white p-2 rounded">
                <X className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <button onClick={handleEdit} className="bg-yellow-500 text-white p-2 rounded">
              <Edit className="h-4 w-4" />
            </button>
          )}
        </div>
        {editing ? (
          <textarea
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            className="w-full h-32 p-2 border border-gray-200 rounded"
          />
        ) : (
          <pre className="p-2 bg-gray-100 rounded">{template.content}</pre>
        )}
      </div>
    </div>
  );
};

export default PromptTemplate;