import React, { useState } from 'react';
import { Book, Settings } from 'lucide-react';
import axiosWithAuth from '../../axiosWithAuth';

const DocumentUploader = () => {
  const [service, setService] = useState('confluence');
  const [workspaceUrl, setWorkspaceUrl] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [spaceKey, setSpaceKey] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const handleUpload = async () => {
    if (!workspaceUrl || !apiKey) {
      setMessage('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setMessage('Authentication token not found');
        return;
      }

      const payload = {
        service,
        workspace_url: workspaceUrl,
        api_key: apiKey,
        space_key: spaceKey
      };

      const endpoint = service === 'confluence'
        ? 'http://127.0.0.1:5000/upload-confluence'
        : 'http://127.0.0.1:5000/upload-notion';

      await axiosWithAuth(token).post(endpoint, payload);

      setMessage(`${service === 'confluence' ? 'Confluence' : 'Notion'} content uploaded successfully!`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      // @ts-ignore
        setMessage(`Error uploading ${service} content: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Book className="h-5 w-5 text-blue-500" />
          <h2 className="text-lg font-semibold">Document Integration</h2>
        </div>
        <button
          onClick={() => setShowSettings(!showSettings)}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <Settings className="h-5 w-5 text-gray-500" />
        </button>
      </div>

      <div className="space-y-4">
        <div className="flex space-x-4 mb-4">
          <button
            onClick={() => setService('confluence')}
            className={`flex-1 py-2 px-4 rounded-lg border transition-colors ${
              service === 'confluence'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-200 hover:bg-gray-50'
            }`}
          >
            Confluence
          </button>
          <button
            onClick={() => setService('notion')}
            className={`flex-1 py-2 px-4 rounded-lg border transition-colors ${
              service === 'notion'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-200 hover:bg-gray-50'
            }`}
          >
            Notion
          </button>
        </div>

        {showSettings && (
          <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {service === 'confluence' ? 'Confluence URL' : 'Notion Workspace URL'}
              </label>
              <input
                type="text"
                value={workspaceUrl}
                onChange={(e) => setWorkspaceUrl(e.target.value)}
                placeholder={service === 'confluence' ? 'https://your-domain.atlassian.net' : 'https://www.notion.so/workspace'}
                className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your API key"
                className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
              />
            </div>

            {service === 'confluence' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Space Key
                </label>
                <input
                  type="text"
                  value={spaceKey}
                  onChange={(e) => setSpaceKey(e.target.value)}
                  placeholder="Enter Confluence space key"
                  className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                />
              </div>
            )}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={isLoading}
          className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-blue-300"
        >
          {isLoading ? 'Uploading...' : `Upload ${service === 'confluence' ? 'Confluence' : 'Notion'} Content`}
        </button>
      </div>

      {message && (
        <div
          className={`mt-4 p-3 rounded-lg ${
            message.includes('Error') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
};

export default DocumentUploader;