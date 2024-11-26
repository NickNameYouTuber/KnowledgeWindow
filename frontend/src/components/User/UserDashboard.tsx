import React, { useState } from 'react';
import { Send, History, Book, Star } from 'lucide-react';
import QueryForm from './QueryForm';

const UserDashboard = () => {
  const [history, setHistory] = useState<{ query: string; response: string }[]>([]);

  const handleHistoryUpdate = (newHistory: { query: string; response: string }[]) => {
    setHistory(newHistory);
  };

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-50 rounded-lg">
              <History className="h-5 w-5 text-blue-500" />
            </div>
            <div>
              <div className="text-sm text-gray-500">Recent Queries</div>
              <div className="text-xl font-semibold">{history.length}</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-green-50 rounded-lg">
              <Star className="h-5 w-5 text-green-500" />
            </div>
            <div>
              <div className="text-sm text-gray-500">Saved Responses</div>
              <div className="text-xl font-semibold">12</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-50 rounded-lg">
              <Book className="h-5 w-5 text-purple-500" />
            </div>
            <div>
              <div className="text-sm text-gray-500">Knowledge Base</div>
              <div className="text-xl font-semibold">Active</div>
            </div>
          </div>
        </div>
      </div>

      {/* Query Interface */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold mb-4">Ask a Question</h2>
        <QueryForm onHistoryUpdate={handleHistoryUpdate} />
      </div>

      {/* History Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <QueryHistory history={history} />
      </div>
    </div>
  );
};

const QueryHistory: React.FC<{ history: { query: string; response: string }[] }> = ({ history }) => {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Recent Questions</h2>
        {history.length > 0 && (
          <button className="text-sm text-blue-500 hover:text-blue-600">
            Clear History
          </button>
        )}
      </div>

      <div className="space-y-4">
        {history.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <History className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>No questions yet. Try asking something!</p>
          </div>
        ) : (
          history.map((item, index) => (
            <div
              key={index}
              className="p-4 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
            >
              <div className="flex items-start space-x-2">
                <div className="p-1 bg-blue-50 rounded">
                  <Send className="h-4 w-4 text-blue-500" />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{item.query}</p>
                  <p className="mt-2 text-gray-600">{item.response}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default UserDashboard;