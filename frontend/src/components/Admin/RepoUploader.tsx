import React, { useState } from 'react';
import axios from 'axios';
import { GitBranch } from 'lucide-react';
import axiosWithAuth from '../../axiosWithAuth';

const RepoUploader = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    if (!repoUrl) {
      setMessage('Please enter a repository URL');
      return;
    }

    setIsUploading(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setMessage('Token not found');
        return;
      }
      await axiosWithAuth(token).post('http://127.0.0.1:5000/upload-repo', { repo_url: repoUrl });
      setMessage('Repository uploaded successfully!');
      setTimeout(() => {
        setRepoUrl('');
        setMessage('');
      }, 3000);
    } catch (error) {
      setMessage('Error uploading repository');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center space-x-2 mb-6">
        <GitBranch className="h-5 w-5 text-blue-500" />
        <h2 className="text-lg font-semibold">Upload Repository</h2>
      </div>

      <div className="space-y-4">
        <input
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="Enter repository URL"
          className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
        />
        <button
          onClick={handleUpload}
          disabled={isUploading}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-blue-300"
        >
          {isUploading ? 'Uploading...' : 'Upload Repository'}
        </button>
      </div>

      {message && (
        <div className={`mt-4 p-3 rounded-lg ${message.includes('Error') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default RepoUploader;