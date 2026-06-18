from database.db_connection import DbConnection
from models.models import ProcessFailed


class AgentDB:
    def __init__(self, connection: DbConnection):
        self.connection = connection


    def create_agent(self, data):
        if not data:
            return None

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = f"INSERT INTO agents ({columns}) VALUES ({placeholders});"
        try:
            cursor.execute(sql, values)
            conn.commit()
            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM agents WHERE id = %s;", (new_id,))
            new_agent = cursor.fetchone()
            return new_agent
        except Exception as e:
            conn.rollback()
            raise ProcessFailed                        #return f"Error as {e}"
        finally:
            cursor.close()
            conn.close()


    def get_all_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM agents;"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()


    def get_agent_by_id(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM agents WHERE id = %s;"
        try:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return row
        except:
            raise Exception
        finally:
            cursor.close()
            conn.close()


    def update_agent(self, id, data):
        if not data:
            return False

        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = f"UPDATE agents SET {set_clause} WHERE id = %s;"
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()


    def deactivate_agent(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET is_active = False WHERE id = %s;"
        try:
            cursor.execute(sql, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()

    def increment_completed(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s;"
        try:
            cursor.execute(sql, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()

    def increment_failed(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s;"
        try:
            cursor.execute(sql, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        if agent:
            total = agent["completed_missions"] + agent["failed_missions"]
            summary = {
                "total": total,
                "failed": agent["failed_missions"],
                "completed": agent["completed_missions"],
                "success_rate": round((agent["completed_missions"]/total) * 100, 2) if total > 0 else 0.0
            }
            return summary
        return None


    def count_active_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT COUNT(*) as count FROM agents WHERE is_active = True;"
        try:
            cursor.execute(sql)
            count = cursor.fetchone()
            return count["count"]
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()





connection_db = DbConnection()
if __name__ == "__main__":
    age_manager = AgentDB(connection_db)
    data1 = {"name": "Yoni", "specialty": "network", "agent_rank": "Commander"}
    print(age_manager.update_agent(56, data1))

    print(age_manager.get_all_agents())
    # print(age_manager.increment_failed(1))
    # print(age_manager.count_active_agents())
    # print(age_manager.increment_completed(1))
    # print(age_manager.get_agent_by_id(1))
    # print(age_manager.get_agent_performance(1))
