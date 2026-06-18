from fastapi import APIRouter
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from database.db_connection import DbConnection

agent_db = AgentDB(DbConnection())
mission_db = MissionDB(DbConnection())

report_router = APIRouter()


@report_router.get("/reports/summary")
def get_summary():
    summary = {
        "active_agents_count": agent_db.count_active_agents(),
        "total_missions": mission_db.count_all_missions(),
        "open_missions": mission_db.count_open_missions(),
        "completed_missions": mission_db.count_by_status('COMPLETED'),
        "failed_missions": mission_db.count_by_status('FAILED'),
        "cancelled_missions": mission_db.count_by_status('CANCELLED')
    }
    return summary

@report_router.get("/reports/missions-by-status")
def get_by_status():
    summary = {
        "open": mission_db.count_by_status('ASSIGNED') + mission_db.count_by_status('IN_PROGRESS'),
        "in_progress": mission_db.count_by_status('IN_PROGRESS'),
        "completed": mission_db.count_by_status('COMPLETED'),
        "failed": mission_db.count_by_status('FAILED'),
        "cancelled": mission_db.count_by_status('CANCELLED')
    }
    return summary

@report_router.get("/reports/top-agent")
def get_top():
    return mission_db.get_top_agent()