import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Upload,
  Code2,
  Palette,
  Layout,
  Copy,
  CheckCheck,
  FileText,
  Edit,
  Trash2,
  Paintbrush,
  CircleDot, Type, Zap
} from 'lucide-react';
import { PromptTemplate } from "../../types";
import axiosWithAuth from '../../axiosWithAuth';
import Modal from 'react-modal';
import PromptTemplates from "./PromptTemplate";

const AdminDashboard = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [files, setFiles] = useState<any[]>([]);
  const [deleteModalIsOpen, setDeleteModalIsOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<number | null>(null);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Token not found');
      return;
    }
    const response = await axiosWithAuth(token).get('http://127.0.0.1:5000/files');
    setFiles(response.data);
  };

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
      if (!token) {
        setMessage('Token not found');
        return;
      }
      await axiosWithAuth(token).post(
        `http://127.0.0.1:5000/upload-${file.name.split('.').pop()}`,
        formData,
        {
          headers: {
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
      setTimeout(() => {
        setFile(null);
        setMessage(null);
        fetchFiles();
      }, 3000);
    } catch (error) {
      setMessage('Error uploading file');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (fileId: number) => {
    setFileToDelete(fileId);
    setDeleteModalIsOpen(true);
  };

  const confirmDelete = async () => {
    if (fileToDelete === null) return;

    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Token not found');
      return;
    }
    try {
      await axiosWithAuth(token).delete(`http://127.0.0.1:5000/files/${fileToDelete}`);
      setMessage('File deleted successfully!');
      fetchFiles();
    } catch (error) {
      setMessage('Error deleting file');
    } finally {
      setDeleteModalIsOpen(false);
      setFileToDelete(null);
    }
  };

  const closeDeleteModal = () => {
    setDeleteModalIsOpen(false);
    setFileToDelete(null);
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
            <Upload className="h-12 w-12 text-gray-400 mb-4"/>
            <div className="text-sm text-gray-600">
              {file ? file.name : 'Drop files here or click to upload'}
            </div>
            <div className="text-sm text-gray-600">
              {file ? '' : 'Available formats: .txt, .pdf, .docx, .xslx, .csv'}
            </div>
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

      {/* File List Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex items-center space-x-2 mb-6">
          <FileText className="h-5 w-5 text-blue-500" />
          <h2 className="text-lg font-semibold">Uploaded Files</h2>
        </div>

        <div className="space-y-4">
          {files.map((file) => (
            <div key={file.id} className="flex items-center justify-between p-4 border-b border-gray-200">
              <div>{file.title}</div>
              <button onClick={() => handleDelete(file.id)} className="text-red-500 hover:text-red-600">
                <Trash2 className="h-5 w-5" />
              </button>
            </div>
          ))}
        </div>
      </div>

      <EmbedCodeGenerator />

      <PromptTemplates /> {/* Добавьте новый компонент */}

      <NeuralNetworkSettings />

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={deleteModalIsOpen}
        onRequestClose={closeDeleteModal}
        contentLabel="Confirm Delete"
        className="bg-white p-6 rounded-lg shadow-lg mx-auto my-10 max-w-md"
        overlayClassName="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      >
        <h2 className="text-lg font-semibold mb-4">Confirm Delete</h2>
        <p className="mb-4">Are you sure you want to delete this file?</p>
        <div className="flex justify-end space-x-4">
          <button onClick={closeDeleteModal} className="bg-gray-300 text-gray-700 px-4 py-2 rounded">
            Cancel
          </button>
          <button onClick={confirmDelete} className="bg-red-500 text-white px-4 py-2 rounded">
            Delete
          </button>
        </div>
      </Modal>
    </div>
  );
};


const EmbedCodeGenerator = () => {
  const [format, setFormat] = useState('small');
  const [color, setColor] = useState('#ffffff');
  const [theme, setTheme] = useState('light');
  const [borderRadius, setBorderRadius] = useState('8');
  const [fontSize, setFontSize] = useState('14');
  const [buttonColor, setButtonColor] = useState('#3B82F6');
  const [inputStyle, setInputStyle] = useState('modern');
  const [animationSpeed, setAnimationSpeed] = useState('300');
  const [copied, setCopied] = useState(false);

  const generateEmbedCode = () => {
    const params = new URLSearchParams({
      format,
      color: encodeURIComponent(color),
      theme,
      borderRadius,
      fontSize,
      buttonColor: encodeURIComponent(buttonColor),
      inputStyle,
      animationSpeed,
    }).toString();

    return `<iframe
  src="http://127.0.0.1:5000/embed?${params}"
  style="width: 100%; height: ${format === 'full' ? '100vh' : '400px'}; border: none;"
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
        <h2 className="text-lg font-semibold">Enhanced Embed Code Generator</h2>
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

        {/* Theme Selection */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Paintbrush className="h-4 w-4" />
            <span>Theme</span>
          </label>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>

        {/* Background Color */}
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

        {/* Button Color */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <CircleDot className="h-4 w-4" />
            <span>Button Color</span>
          </label>
          <div className="flex space-x-2">
            <input
              type="color"
              value={buttonColor}
              onChange={(e) => setButtonColor(e.target.value)}
              className="h-10 w-20 rounded border border-gray-200 p-1"
            />
            <input
              type="text"
              value={buttonColor}
              onChange={(e) => setButtonColor(e.target.value)}
              className="flex-1 px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
        </div>

        {/* Border Radius */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Layout className="h-4 w-4" />
            <span>Border Radius (px)</span>
          </label>
          <input
            type="range"
            min="0"
            max="20"
            value={borderRadius}
            onChange={(e) => setBorderRadius(e.target.value)}
            className="w-full"
          />
          <div className="text-sm text-gray-500 text-right">{borderRadius}px</div>
        </div>

        {/* Font Size */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Type className="h-4 w-4" />
            <span>Font Size (px)</span>
          </label>
          <input
            type="range"
            min="12"
            max="20"
            value={fontSize}
            onChange={(e) => setFontSize(e.target.value)}
            className="w-full"
          />
          <div className="text-sm text-gray-500 text-right">{fontSize}px</div>
        </div>

        {/* Input Style */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Layout className="h-4 w-4" />
            <span>Input Style</span>
          </label>
          <select
            value={inputStyle}
            onChange={(e) => setInputStyle(e.target.value)}
className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
          >
            <option value="modern">Modern</option>
            <option value="minimal">Minimal</option>
            <option value="classic">Classic</option>
          </select>
        </div>

        {/* Animation Speed */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Zap className="h-4 w-4" />
            <span>Animation Speed (ms)</span>
          </label>
          <select
            value={animationSpeed}
            onChange={(e) => setAnimationSpeed(e.target.value)}
            className="w-full px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
          >
            <option value="150">Fast (150ms)</option>
            <option value="300">Normal (300ms)</option>
            <option value="500">Slow (500ms)</option>
          </select>
        </div>

        {/* Preview */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
            <Layout className="h-4 w-4" />
            <span>Preview</span>
          </label>
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <iframe
              src={`http://127.0.0.1:5000/embed?${new URLSearchParams({
                format,
                color: encodeURIComponent(color),
                theme,
                borderRadius,
                fontSize,
                buttonColor: encodeURIComponent(buttonColor),
                inputStyle,
                animationSpeed,
              }).toString()}`}
              style={{ width: '100%', height: '300px', border: 'none' }}
              title="Embed Preview"
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

const NeuralNetworkSettings = () => {
  const [settings, setSettings] = useState({ url: '', api_key: '', model: '' });
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found');
      return;
    }
    const response = await axiosWithAuth(token).get('http://127.0.0.1:5000/neural-network/settings');
    setSettings(response.data);
  };

  const handleUpdate = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found');
      return;
    }
    await axiosWithAuth(token).post('http://127.0.0.1:5000/neural-network/settings', settings);
    setEditing(false);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center space-x-2 mb-6">
        <FileText className="h-5 w-5 text-blue-500" />
        <h2 className="text-lg font-semibold">Neural Network Settings</h2>
      </div>

      <div className="space-y-6">
        {editing ? (
          <>
            <input
              type="text"
              value={settings.url}
              onChange={(e) => setSettings({ ...settings, url: e.target.value })}
              placeholder="URL"
              className="border p-2 w-full mb-2"
            />
            <input
              type="text"
              value={settings.api_key}
              onChange={(e) => setSettings({ ...settings, api_key: e.target.value })}
              placeholder="API Key"
              className="border p-2 w-full mb-2"
            />
            <input
              type="text"
              value={settings.model}
              onChange={(e) => setSettings({ ...settings, model: e.target.value })}
              placeholder="Model"
              className="border p-2 w-full mb-2"
            />
            <button onClick={handleUpdate} className="bg-green-500 text-white p-2 mr-2">
              Save
            </button>
            <button onClick={() => setEditing(false)} className="bg-red-500 text-white p-2">
              Cancel
            </button>
          </>
        ) : (
          <>
            <div className="font-bold">URL: {settings.url}</div>
            <div className="font-bold">API Key: {settings.api_key}</div>
            <div className="font-bold">Model: {settings.model}</div>
            <button onClick={() => setEditing(true)} className="bg-yellow-500 text-white p-2">
              <Edit className="h-4 w-4" />
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;