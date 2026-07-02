'use client';

import { create } from 'zustand';

interface MarketData {
  symbol: string;
  price: number;
  change24h: number;
  high24h: number;
  low24h: number;
  volume24h: number;
}

interface Position {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  quantity: number;
  entryPrice: number;
  currentPrice: number;
  unrealizedPnL: number;
}

interface Trade {
  id: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  entryPrice: number;
  exitPrice?: number;
  pnl: number;
  status: 'OPEN' | 'CLOSED';
  agent: string;
  timestamp: string;
}

interface TradingStore {
  marketData: Map<string, MarketData>;
  positions: Position[];
  trades: Trade[];
  portfolio: {
    totalBalance: number;
    availableBalance: number;
    unrealizedPnL: number;
    realizedPnL: number;
  };
  setMarketData: (data: MarketData) => void;
  addPosition: (position: Position) => void;
  updatePosition: (id: string, position: Partial<Position>) => void;
  removePosition: (id: string) => void;
  addTrade: (trade: Trade) => void;
  updatePortfolio: (updates: any) => void;
}

export const useTradingStore = create<TradingStore>((set) => ({
  marketData: new Map(),
  positions: [],
  trades: [],
  portfolio: {
    totalBalance: 0,
    availableBalance: 0,
    unrealizedPnL: 0,
    realizedPnL: 0,
  },
  setMarketData: (data) =>
    set((state) => {
      const newMap = new Map(state.marketData);
      newMap.set(data.symbol, data);
      return { marketData: newMap };
    }),
  addPosition: (position) =>
    set((state) => ({
      positions: [...state.positions, position],
    })),
  updatePosition: (id, updates) =>
    set((state) => ({
      positions: state.positions.map((p) =>
        p.id === id ? { ...p, ...updates } : p
      ),
    })),
  removePosition: (id) =>
    set((state) => ({
      positions: state.positions.filter((p) => p.id !== id),
    })),
  addTrade: (trade) =>
    set((state) => ({
      trades: [trade, ...state.trades],
    })),
  updatePortfolio: (updates) =>
    set((state) => ({
      portfolio: { ...state.portfolio, ...updates },
    })),
}));
