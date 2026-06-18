from fastapi import APIRouter, HTTPException

from routes.agent_routes import agent_db
from services.utils import calculate_risk_level
from models.models import Mission
from database.mission_db import MissionDB
from database.db_connection import DbConnection

mission_db = MissionDB(DbConnection())

mission_router = APIRouter()


@mission_router.post("/missions", status_code=201)
def post_mission(data: Mission):
    data = data.model_dump()
    if  0 >= data["difficulty"] or data["difficulty"] > 10 \
    or  0 >= data["importance"] or data["importance"] > 10:
        raise HTTPException(status_code=400,detail="Wrong values")

    data["risk_level"] = calculate_risk_level(data["difficulty"], data["importance"])
    mission = mission_db.create_mission(data)
    return mission


@mission_router.get("/missions")
def get_all_missions():
    return mission_db.get_all_missions()


@mission_router.get("/missions/{id}")
def get_mission_by_id(id: int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@mission_router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(mission_id: int, agent_id: int):
    mission = mission_db.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    agent = agent_db.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if mission["status"] != 'NEW':
        raise HTTPException(status_code=400, detail="Bad request")
    if not agent["is_active"]:
        raise HTTPException(status_code=400, detail="Bad request")
    open_missions = mission_db.get_open_missions_by_agent(agent_id)
    if len(open_missions) >= mission_db.MAX_OPEN_MISSIONS:
        raise HTTPException(status_code=400, detail="Bad request")
    if mission["risk_level"] == 'CRITICAL' and \
            agent["agent_rank"] == 'JUNIOR' or agent["agent_rank"] == 'SENIOR':
        raise HTTPException(status_code=400, detail="Bad request")

    mission_db.assign_mission(mission_id, agent_id)
    mission_db.update_mission_status(mission_id, 'ASSIGNED')
    return 'ASSIGNED'


@mission_router.put("/missions/{id}/start")
def start_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not mission["status"] == 'ASSIGNED':
        raise HTTPException(status_code=400, detail="Bad request")
    mission_db.update_mission_status(id, 'IN_PROGRESS')
    return 'IN_PROGRESS'


@mission_router.put("/missions/{id}/complete")
def complete_mission(id:int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not mission["status"] == 'IN_PROGRESS':
        raise HTTPException(status_code=400, detail="Bad request")
    mission_db.update_mission_status(id, 'COMPLETED')
    agent_id = mission["assigned_agent_id"]
    agent_db.increment_completed(agent_id)
    return 'COMPLETED'


@mission_router.put("/missions/{id}/fail")
def fail_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not mission["status"] == 'IN_PROGRESS':
        raise HTTPException(status_code=400, detail="Bad request")
    mission_db.update_mission_status(id,'FAILED')
    agent_id = mission["assigned_agent_id"]
    agent_db.increment_failed(agent_id)
    return 'FAILED'


@mission_router.put("/missions/{id}/cancel")
def cancel_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission["status"] != ('ASSIGNED' or 'NEW'):
        raise HTTPException(status_code=400, detail="Bad request")
    mission_db.update_mission_status(id, 'CANCELLED')
    return 'CANCELLED'



