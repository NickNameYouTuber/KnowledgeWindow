import React, { useState } from 'react';

const EmbedCodeGenerator = () => {
  const [format, setFormat] = useState('small');
  const [color, setColor] = useState('#ffffff');

  const generateEmbedCode = () => {
    const iframeCode = `
      <iframe
        src="http://127.0.0.1:5000/embed?format=${format}&color=${encodeURIComponent(color)}"
        style="width: 100%; height: ${format === 'full' ? '100vh' : '300px'}; border: none;"
      ></iframe>
    `;

    return iframeCode.trim();
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Embed Code Generator</h2>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Format</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="border p-2 w-full"
          >
            <option value="small">Small Window</option>
            <option value="full">Full Page</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Color</label>
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="border p-2 w-full"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Embed Code</label>
          <textarea
            readOnly
            value={generateEmbedCode()}
            className="border p-2 w-full h-32"
          />
        </div>
      </div>
    </div>
  );
};

export default EmbedCodeGenerator;