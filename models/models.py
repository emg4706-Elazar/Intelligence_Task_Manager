from pydantic import BaseModel
from typing import Literal

class Agent(BaseModel):
    name: str
    specialty: str
    agent_rank: Literal['Junior', 'Senior', 'Commander']



class Mission(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int



class AgentNotFound(Exception):
    pass

class ProcessFailed(Exception):
    pass








