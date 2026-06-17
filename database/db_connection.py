import mysql.connector


class DbConnection:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "1234"

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="intelligence_db"
        )

    def create_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS intelligence_db;"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return

    def create_tables(self, sql1, sql2):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
        conn.commit()
        cursor.close()
        conn.close()
        return





q_agents = """
CREATE TABLE IF NOT EXISTS agents (
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
specialty VARCHAR(50) NOT NULL,
is_active BOOLEAN DEFAULT TRUE,
completed_missions INT DEFAULT 0,
failed_missions INT DEFAULT 0,
agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
);
"""

q_missions = """
CREATE TABLE IF NOT EXISTS missions (
id INT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(50) NOT NULL,
description TEXT NOT NULL,
location VARCHAR(100),
difficulty INT NOT NULL,
importance INT NOT NULL,
status ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'NEW',
risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
assigned_agent_id   INT
);
"""


if __name__ == "__main__":
    db_connection = DbConnection()
    db_connection.create_database()
    db_connection.create_tables(q_agents, q_missions)
