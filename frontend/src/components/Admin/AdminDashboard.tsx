import React from 'react';
import { Link } from 'react-router-dom';
import {
  FileText,
  Users,
  Database,
  BarChart3,
  ArrowRight
} from 'lucide-react';

const AdminDashboard = () => {
  const stats = [
    { label: 'Total Users', value: '1,234' },
    { label: 'Active Sessions', value: '56' },
    { label: 'Templates', value: '25' },
    { label: 'Queries Today', value: '892' },
  ];

  const features = [
    {
      title: 'Prompt Templates',
      icon: FileText,
      description: 'Manage and customize prompt templates',
      link: '/admin/prompt-templates'
    },
    {
      title: 'User Management',
      icon: Users,
      description: 'Manage user accounts and permissions',
      link: '/admin/users'
    },
    {
      title: 'Knowledge Base',
      icon: Database,
      description: 'Update and maintain knowledge base',
      link: '/admin/knowledge-base'
    },
    {
      title: 'Statistics',
      icon: BarChart3,
      description: 'View system analytics and metrics',
      link: '/admin/statistics'
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <div className="text-sm text-gray-500">{stat.label}</div>
            <div className="text-2xl font-semibold mt-1">{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((feature, index) => (
          <Link
            key={index}
            to={feature.link}
            className="group bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all"
          >
            <div className="flex items-center justify-between">
              <feature.icon className="h-6 w-6 text-blue-500" />
              <ArrowRight className="h-4 w-4 text-gray-400 group-hover:translate-x-1 transition-transform" />
            </div>
            <h3 className="text-lg font-semibold mt-4 mb-2">{feature.title}</h3>
            <p className="text-sm text-gray-500">{feature.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;