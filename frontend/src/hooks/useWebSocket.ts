'use client';

import { useEffect, useState } from 'react';
import { useTradingStore } from '@/store/tradingStore';

interface WebSocketMessage {
  type: 'market_data' | 'trade' | 'position' | 'alert';
  data: any;
}

export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const store = useTradingStore();

  useEffect(() => {
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws');

    ws.onopen = () => {
      console.log('✅ WebSocket connected');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);

        switch (message.type) {
          case 'market_data':
            store.setMarketData(message.data);
            break;
          case 'trade':
            store.addTrade(message.data);
            break;
          case 'position':
            store.updatePosition(message.data.id, message.data);
            break;
          case 'alert':
            console.log('🔔 Alert:', message.data);
            break;
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };

    ws.onerror = () => {
      console.error('❌ WebSocket error');
      setConnected(false);
    };

    ws.onclose = () => {
      console.log('❌ WebSocket disconnected');
      setConnected(false);
      // Attempt reconnection after 3 seconds
      setTimeout(() => {
        console.log('🔄 Reconnecting...');
      }, 3000);
    };

    return () => {
      ws.close();
    };
  }, [store]);

  return { connected };
}
