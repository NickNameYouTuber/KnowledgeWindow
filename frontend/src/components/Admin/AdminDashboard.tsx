import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Code2, Palette, Layout, Copy, CheckCheck } from 'lucide-react';

const AdminDashboard = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setUploadProgress(0);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `http://127.0.0.1:5000/upload-${file.name.split('.').pop()}`, 
        formData, 
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total
              ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
              : 0;
            setUploadProgress(progress);
          },
        }
      );
      setMessage('File uploaded successfully!');
    } catch (error) {
      setMessage('Error uploading file');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* File Upload Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex items-center space-x-2 mb-6">
          <Upload className="h-5 w-5 text-blue-500" />
          <h2 className="text-lg font-semibold">Upload Knowledge Base</h2>
        </div>
        
        <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center">
          <input
            type="file"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <Upload className="h-12 w-12 text-gray-400 mb-4" />
            <span className="text-sm text-gray-600">
              {file ? file.name : 'Drop files here or click to upload'}
            </span>
          </label>
          
          {file && (
            <div className="mt-4">
              <div className="w-full bg-gray-100 rounded-full h-2 mb-4">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-blue-300"
              >
                {isUploading ? 'Uploading...' : 'Upload File'}
              </button>
            </div>
          )}
        </div>
        
        {message && (
          <div className={`mt-4 p-3 rounded-lg ${message.includes('Error') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
            {message}
          </div>
        )}
      </div>

      <EmbedCodeGenerator />
    </div>
  );
};

const EmbedCodeGenerator = () => {
  const [format, setFormat] = useState('small');
  const [color, setColor] = useState('#ffffff');
  const [copied, setCopied] = useState(false);

  const generateEmbedCode = () => {
    return `<iframe
  src="http://127.0.0.1:5000/embed?format=${format}&color=${encodeURIComponent(color)}"
  style="width: 100%; height: ${format === 'full' ? '100vh' : '300px'}; border: none;"
></iframe>`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generateEmbedCode());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center space-x-2 mb-6">
        <Code2 className="h-5 w-5 text-blue-500" />
        <h2 className="text-lg font-semibold">Embed Code Generator</h2>
      </div>

      <div className="space-y-6">
        {/* Format Selection */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Layout className="h-4 w-4" />
            <span>Format</span>
          </label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
          >
            <option value="small">Small Window</option>
            <option value="full">Full Page</option>
          </select>
        </div>

        {/* Color Selection */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Palette className="h-4 w-4" />
            <span>Background Color</span>
          </label>
          <div className="flex space-x-2">
            <input
              type="color"
              value={color}
              onChange={(e) => setColor(e.target.value)}
              className="h-10 w-20 rounded border border-gray-200 p-1"
            />
            <input
              type="text"
              value={color}
              onChange={(e) => setColor(e.target.value)}
              className="flex-1 px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
        </div>

        {/* Generated Code */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
              <Code2 className="h-4 w-4" />
              <span>Generated Code</span>
            </label>
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 text-sm text-blue-500 hover:text-blue-600 transition-colors"
            >
              {copied ? (
                <>
                  <CheckCheck className="h-4 w-4" />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4" />
                  <span>Copy code</span>
                </>
              )}
            </button>
          </div>
          <div className="relative">
            <textarea
              readOnly
              value={generateEmbedCode()}
              className="w-full h-32 px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all font-mono text-sm bg-gray-50"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;