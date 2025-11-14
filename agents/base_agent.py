import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from config.settings import settings

logger = logging.getLogger(__name__)

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    RECOVERING = "recovering"
    COMPLETED = "completed"

@dataclass
class AgentState:
    """Agent execution state tracking"""
    agent_name: str
    status: AgentStatus = AgentStatus.IDLE
    error_count: int = 0
    last_error: Optional[str] = None
    execution_history: List[Dict] = field(default_factory=list)
    data_collected: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class BaseAgent:
    """Advanced agent with comprehensive error recovery"""
    
    def __init__(
        self,
        name: str,
        role: str,
        goals: List[str],
        tools: List[Any],
        system_prompt: str,
        max_errors: int = 3,
        timeout: int = None
    ):
        self.name = name
        self.role = role
        self.goals = goals
        self.tools = tools
        self.system_prompt = system_prompt
        self.max_errors = max_errors
        self.timeout = timeout or settings.AGENT_TIMEOUT
        
        self.state = AgentState(agent_name=name)
        
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.executor = None
        self._initialize()
    
    def _initialize(self):
        """Initialize agent"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            agent = create_openai_functions_agent(
                self.llm,
                self.tools,
                prompt
            )
            
            self.executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                memory=self.memory,
                verbose=settings.DEBUG,
                handle_parsing_errors=True,
                max_iterations=15
            )
            
            logger.info(f"✓ Initialized: {self.name}")
            self.state.status = AgentStatus.IDLE
            
        except Exception as e:
            logger.error(f"✗ Failed to initialize {self.name}: {e}")
            self.state.status = AgentStatus.ERROR
            self.state.last_error = str(e)
            raise
    
    async def execute(
        self,
        task: str,
        context: Dict[str, Any] = None,
        company_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute task with comprehensive error handling"""
        
        if self.state.error_count >= self.max_errors:
            return {
                "status": "failed",
                "error": f"Max errors ({self.max_errors}) exceeded",
                "agent": self.name,
                "error_count": self.state.error_count
            }
        
        try:
            self.state.status = AgentStatus.RUNNING
            self.state.start_time = datetime.now()
            
            enhanced_task = f"""
{task}

ANTI-HALLUCINATION RULES:
1. ONLY use data from tool outputs
2. If no data, state "No data available for [item]"
3. Cite tool name for each fact
4. Mark confidence: [HIGH] >80%, [MEDIUM] 50-80%, [LOW] <50%
5. NEVER fabricate numbers or statistics
6. Flag contradictions between sources

Company Context:
{company_info or {}}

Additional Context:
{context or {}}
"""
            
            try:
                result = await asyncio.wait_for(
                    self._run_executor(enhanced_task),
                    timeout=self.timeout
                )
                
                self.state.status = AgentStatus.COMPLETED
                self.state.error_count = 0
                self.state.end_time = datetime.now()
                self.state.execution_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "task_summary": task[:100],
                    "duration": (self.state.end_time - self.state.start_time).total_seconds()
                })
                
                return {
                    "status": "success",
                    "agent": self.name,
                    "result": result,
                    "timestamp": datetime.now().isoformat(),
                    "duration_seconds": (self.state.end_time - self.state.start_time).total_seconds()
                }
                
            except asyncio.TimeoutError:
                raise Exception(f"Task timeout after {self.timeout}s")
        
        except Exception as e:
            logger.error(f"Agent {self.name} error: {e}")
            self.state.status = AgentStatus.ERROR
            self.state.error_count += 1
            self.state.last_error = str(e)
            self.state.end_time = datetime.now()
            
            if self.state.error_count < self.max_errors:
                logger.info(f"Recovering {self.name} (attempt {self.state.error_count}/{self.max_errors})")
                self.state.status = AgentStatus.RECOVERING
                await asyncio.sleep(settings.AGENT_RETRY_DELAY ** self.state.error_count)
                
                self._initialize()
                return await self.execute(task, context, company_info)
            
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "error_count": self.state.error_count,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _run_executor(self, task: str) -> str:
        """Run executor in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.executor.invoke({"input": task})["output"]
        )
    
    def get_state(self) -> AgentState:
        """Get current agent state"""
        return self.state
    
    def reset(self):
        """Reset agent"""
        self.state = AgentState(agent_name=self.name)
        self.memory.clear()
        self._initialize()
        logger.info(f"Reset: {self.name}")