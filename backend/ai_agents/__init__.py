"""AI Agents module."""
from backend.ai_agents.orchestrator import AgentOrchestrator
from backend.ai_agents.momentum_scalper import MomentumScalperAgent
from backend.ai_agents.orderflow_ai import OrderFlowAgent
from backend.ai_agents.meanreversion_ai import MeanReversionAgent
from backend.ai_agents.sentiment_ai import SentimentAgent
from backend.ai_agents.whale_tracker import WhaleTrackerAgent


class AIAgentsSystem:
    """Central AI agents system."""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.momentum_agent = MomentumScalperAgent()
        self.orderflow_agent = OrderFlowAgent()
        self.meanreversion_agent = MeanReversionAgent()
        self.sentiment_agent = SentimentAgent()
        self.whale_agent = WhaleTrackerAgent()
        
        # Register agents with orchestrator
        self.orchestrator.register_agent(self.momentum_agent)
        self.orchestrator.register_agent(self.orderflow_agent)
        self.orchestrator.register_agent(self.meanreversion_agent)
        self.orchestrator.register_agent(self.sentiment_agent)
        self.orchestrator.register_agent(self.whale_agent)
    
    async def initialize(self):
        """Initialize all agents."""
        await self.orchestrator.start()
    
    async def shutdown(self):
        """Shutdown all agents."""
        await self.orchestrator.stop()
    
    async def get_trading_signal(self, market_data):
        """Get consensus trading signal from all agents."""
        return await self.orchestrator.get_consensus_signal(market_data)


async def init_agents():
    """Initialize AI agents system."""
    system = AIAgentsSystem()
    await system.initialize()
    return system
