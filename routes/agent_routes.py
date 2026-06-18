from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.db_connection import DbConnection
from models.models import Agent, ProcessFailed



agent_db = AgentDB(DbConnection())

agent_router = APIRouter()

@agent_router.post("/agents", status_code=201)
def post_agent(data: Agent):
    data = data.model_dump()
    try:
        new_agent = agent_db.create_agent(data)
        return new_agent
    except ProcessFailed:
        raise HTTPException(status_code=500, detail="Unknown exception")


@agent_router.get("/agents")
def get_all_agents():
    return agent_db.get_all_agents()


@agent_router.get("/agents/{id}")
def get_agent_by_id(id: int):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@agent_router.put("/agents/{id}")
def put_agent(id, data: Agent):
    data = data.model_dump()
    updated = agent_db.update_agent(id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Agent not found")
    return "Agent was updated successfully"



# @agent_router.put("/agents/{id}/deactivate")
#
#
# @agent_router.put("/agents/{id}/performance")








