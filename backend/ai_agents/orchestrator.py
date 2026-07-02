"""Central AI Consensus Engine - Orchestrates all trading agents."""
import logging
from typing import List, Dict
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Central orchestration engine for AI agents."""
    
    def __init__(self):
        self.agents: List = []
        self.is_running = False
        self.consensus_threshold = 0.70  # 70% confidence required
        self.trade_history = []
    
    def register_agent(self, agent):
        """Register a new agent."""
        self.agents.append(agent)
        logger.info(f"✅ Registered agent: {agent.name}")
    
    async def start(self):
        """Start the orchestrator."""
        self.is_running = True
        logger.info("🚀 AI Consensus Engine started")
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    async def stop(self):
        """Stop the orchestrator."""
        self.is_running = False
        logger.info("🛑 AI Consensus Engine stopped")
    
    async def get_consensus_signal(self, market_data: Dict):
        """Get consensus trading signal from all agents."""
        signals = []
        confidences = []
        
        # Collect signals from all agents
        for agent in self.agents:
            try:
                signal = await agent.analyze(market_data)
                if signal:
                    signals.append(signal)
                    confidences.append(signal.get('confidence', 0))
                    logger.debug(f"Signal from {agent.name}: {signal['action']} ({signal['confidence']:.1%})")
            except Exception as e:
                logger.error(f"Error from {agent.name}: {e}")
        
        # Calculate consensus
        if not signals:
            return None
        
        consensus = self._calculate_consensus(signals, confidences)
        
        # Only execute if confidence threshold met
        if consensus['final_confidence'] >= self.consensus_threshold:
            logger.info(f"✅ TRADE APPROVED - Confidence: {consensus['final_confidence']:.1%}")
            return consensus
        else:
            logger.info(f"❌ Trade skipped - Low confidence: {consensus['final_confidence']:.1%}")
            return None
    
    def _calculate_consensus(self, signals: List[Dict], confidences: List[float]) -> Dict:
        """Calculate consensus from agent signals."""
        # Count agreements
        buys = sum(1 for s in signals if s['action'] == 'BUY')
        sells = sum(1 for s in signals if s['action'] == 'SELL')
        
        # Determine action
        if buys > sells:
            final_action = 'BUY'
            agreement_count = buys
        elif sells > buys:
            final_action = 'SELL'
            agreement_count = sells
        else:
            final_action = 'NEUTRAL'
            agreement_count = 0
        
        # Average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Agreement ratio
        agreement_ratio = agreement_count / len(signals) if signals else 0
        
        # Final confidence = average confidence * agreement ratio
        final_confidence = avg_confidence * agreement_ratio
        
        return {
            'final_action': final_action,
            'final_confidence': final_confidence,
            'agreement_ratio': agreement_ratio,
            'agent_count': len(signals),
            'signals': signals,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _monitoring_loop(self):
        """Continuous monitoring of agent health."""
        while self.is_running:
            try:
                for agent in self.agents:
                    health = await agent.get_health()
                    if health['status'] == 'unhealthy':
                        logger.warning(f"⚠️  Agent {agent.name} is unhealthy")
                        await agent.recover()
                await asyncio.sleep(60)  # Check every 60 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)
