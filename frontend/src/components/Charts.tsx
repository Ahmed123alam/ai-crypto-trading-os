'use client';

import React from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ChartProps {
  data: any[];
  title?: string;
  height?: number;
}

export function PriceChart({ data, title, height = 300 }: ChartProps) {
  return (
    <div className="w-full bg-dark-card rounded-lg p-4 card-glow">
      {title && <h3 className="text-neon-green mb-4 font-bold">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 255, 65, 0.1)" />
          <XAxis stroke="rgba(0, 255, 65, 0.5)" />
          <YAxis stroke="rgba(0, 255, 65, 0.5)" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1f3a',
              border: '1px solid #00ff41',
              borderRadius: '4px',
            }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#00ff41"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function PnLChart({ data, title, height = 300 }: ChartProps) {
  return (
    <div className="w-full bg-dark-card rounded-lg p-4 card-glow-blue">
      {title && <h3 className="text-neon-blue mb-4 font-bold">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 212, 255, 0.1)" />
          <XAxis stroke="rgba(0, 212, 255, 0.5)" />
          <YAxis stroke="rgba(0, 212, 255, 0.5)" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1f3a',
              border: '1px solid #00d4ff',
              borderRadius: '4px',
            }}
          />
          <Area
            type="monotone"
            dataKey="pnl"
            stroke="#00d4ff"
            fill="rgba(0, 212, 255, 0.1)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export function VolumChart({ data, title, height = 300 }: ChartProps) {
  return (
    <div className="w-full bg-dark-card rounded-lg p-4 card-glow">
      {title && <h3 className="text-neon-green mb-4 font-bold">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 255, 65, 0.1)" />
          <XAxis stroke="rgba(0, 255, 65, 0.5)" />
          <YAxis stroke="rgba(0, 255, 65, 0.5)" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1f3a',
              border: '1px solid #00ff41',
              borderRadius: '4px',
            }}
          />
          <Bar dataKey="volume" fill="#00ff41" radius={4} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
