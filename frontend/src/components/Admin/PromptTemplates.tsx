import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface PromptTemplate {
  id: number;
  name: string;
  template: string;
}

const PromptTemplates = () => {
  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [newTemplate, setNewTemplate] = useState({ name: '', template: '' });
  const [editingTemplate, setEditingTemplate] = useState<PromptTemplate | null>(null);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    const response = await axios.get('http://127.0.0.1:5000/templates');
    setTemplates(response.data);
  };

  const handleCreate = async () => {
    await axios.post('http://127.0.0.1:5000/templates', newTemplate);
    setNewTemplate({ name: '', template: '' });
    fetchTemplates();
  };

  const handleUpdate = async (id: number) => {
    if (editingTemplate) {
      await axios.put(`http://127.0.0.1:5000/templates/${id}`, editingTemplate);
      setEditingTemplate(null);
      fetchTemplates();
    }
  };

  const handleDelete = async (id: number) => {
    await axios.delete(`http://127.0.0.1:5000/templates/${id}`);
    fetchTemplates();
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Create New Template</h2>
        <input
          type="text"
          value={newTemplate.name}
          onChange={(e) => setNewTemplate({ ...newTemplate, name: e.target.value })}
          placeholder="Template Name"
          className="border p-2 w-full mb-2"
        />
        <textarea
          value={newTemplate.template}
          onChange={(e) => setNewTemplate({ ...newTemplate, template: e.target.value })}
          placeholder="Template Content"
          className="border p-2 w-full mb-2"
        />
        <button onClick={handleCreate} className="bg-blue-500 text-white p-2">
          Create
        </button>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Templates</h2>
        {templates.map((template) => (
          <div key={template.id} className="border p-2 mb-2">
            {editingTemplate?.id === template.id ? (
              <>
                <input
                  type="text"
                  value={editingTemplate.name}
                  onChange={(e) => setEditingTemplate({ ...editingTemplate, name: e.target.value })}
                  className="border p-2 w-full mb-2"
                />
                <textarea
                  value={editingTemplate.template}
                  onChange={(e) => setEditingTemplate({ ...editingTemplate, template: e.target.value })}
                  className="border p-2 w-full mb-2"
                />
                <button onClick={() => handleUpdate(template.id)} className="bg-green-500 text-white p-2 mr-2">
                  Save
                </button>
                <button onClick={() => setEditingTemplate(null)} className="bg-red-500 text-white p-2">
                  Cancel
                </button>
              </>
            ) : (
              <>
                <div className="font-bold">{template.name}</div>
                <div>{template.template}</div>
                <button onClick={() => setEditingTemplate(template)} className="bg-yellow-500 text-white p-2 mr-2">
                  Edit
                </button>
                <button onClick={() => handleDelete(template.id)} className="bg-red-500 text-white p-2">
                  Delete
                </button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PromptTemplates;