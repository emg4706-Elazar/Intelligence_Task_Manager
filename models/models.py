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
    difficulty: Literal[1, 2, 3, 4, 5, 6, 7,8, 9, 10]
    importance: Literal[1, 2, 3, 4, 5, 6, 7,8, 9, 10]



class AgentNotFound(Exception):
    pass

class ProcessFailed(Exception):
    pass








