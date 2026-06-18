from fastapi import FastAPI
from routes.agent_routes import agent_router
from routes.mission_routes import mission_router
from routes.report_routes import report_router
from database.db_connection import DbConnection, q_agents, q_missions
import uvicorn
from logs.logging_config import logger

app = FastAPI()

app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)

connection = DbConnection()
connection.create_database()
connection.create_tables(q_agents, q_missions)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
