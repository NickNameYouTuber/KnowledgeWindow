import React, { useState } from 'react';
import {
  Brain,
  Zap,
  Clock,
  Shield,
  ChevronRight,
  Mail,
  Lock,
  User
} from 'lucide-react';
import axios from "axios";
import {useAuth} from "../AuthContext";
import LoginForm from "./Auth/LoginForm";
import RegisterForm from "./Auth/RegisterForm";

const HomePage = () => {
  const [isLoginMode, setIsLoginMode] = useState(false);

  const features = [
    {
      icon: Brain,
      title: "Advanced AI Integration",
      description: "Powered by state-of-the-art AI models for accurate and relevant responses"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Get instant responses to your queries with our optimized system"
    },
    {
      icon: Clock,
      title: "24/7 Availability",
      description: "Access information and get answers whenever you need them"
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "Your data is encrypted and protected with enterprise-grade security"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          {/* Left side - Content */}
          <div className="flex-1 space-y-6">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Your Smart AI Assistant for
              <span className="text-blue-500"> Instant Answers</span>
            </h1>
            <p className="text-lg text-gray-600">
              Get accurate answers instantly with our advanced AI-powered platform.
              Perfect for research, learning, and problem-solving.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setIsLoginMode(true)}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
              >
                Get Started <ChevronRight className="h-4 w-4" />
              </button>
              <button
                onClick={() => setIsLoginMode(false)}
                className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Learn More
              </button>
            </div>
          </div>

          {/* Right side - Auth Form */}
          <div className="flex-1">
            <div className="bg-white p-8 rounded-2xl shadow-lg max-w-md mx-auto">
              {isLoginMode ? <LoginForm /> : <RegisterForm />}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why Choose Our Platform</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="p-6 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-blue-500" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;