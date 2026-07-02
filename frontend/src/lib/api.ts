'use client';

import axios, { AxiosInstance } from 'axios';

const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to headers if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Trades
  getTrades: () => apiClient.get('/api/trades'),
  createTrade: (data: any) => apiClient.post('/api/trades', data),
  getTrade: (id: string) => apiClient.get(`/api/trades/${id}`),
  closeTrade: (id: string) => apiClient.post(`/api/trades/${id}/close`),

  // Portfolio
  getPortfolio: () => apiClient.get('/api/portfolio'),
  getPositions: () => apiClient.get('/api/portfolio/positions'),
  getPerformance: () => apiClient.get('/api/portfolio/performance'),

  // Agents
  getAgents: () => apiClient.get('/api/agents'),
  getAgentSignals: () => apiClient.get('/api/agents/signals'),
  getAgentPerformance: (agentName: string) =>
    apiClient.get(`/api/agents/${agentName}/performance`),

  // Strategies
  getStrategies: () => apiClient.get('/api/strategies'),
  createStrategy: (data: any) => apiClient.post('/api/strategies', data),
  updateStrategy: (id: string, data: any) =>
    apiClient.put(`/api/strategies/${id}`, data),

  // Health
  getHealth: () => apiClient.get('/api/health'),
};

export default apiClient;
