from database.db_connection import DbConnection



class AgentDB:
    def __init__(self, connection: DbConnection):
        self.connection = DbConnection()


    def create_agent(self, data):
        columns = list([str(key) for key in data])
        values = list([data[key] for key in data])
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO agents (%s) VALUES %s;
        """
        cursor.execute(sql, (columns, values))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("""
        SELECT * FROM agents WHERE id = %s """, new_id)
        new_agent = cursor.fetchone()
        cursor.close()
        conn.close()
        return new_agent

    def get_all_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM agents;"""
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()


    def get_agent_by_id(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM agents WHERE id = %s;"""
        try:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()


    def update_agent(self, id, data):
        columns = list([str(key) for key in data])
        values = list([data[key] for key in data])
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE agents (%s) VALUES %s WHERE id = %s;
        """
        cursor.execute(sql, (columns, values, id))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()
        return rowcount > 0

    def deactivate_agent(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET is_active = False WHERE id = %s;"
        try:
            cursor.execute(sql, (id,))
            conn.commit()
            rowcount = cursor.rowcount
            return rowcount > 0
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()

    def increment_completed(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET completed_missions = %s WHERE id = %s;"
        try:
            completed_missions = self.get_agent_by_id(id)["completed_missions"]
            completed_missions += 1
            cursor.execute(sql, (completed_missions, id))
            conn.commit()
            rowcount = cursor.rowcount
            return rowcount > 0
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()

    def increment_failed(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET failed_missions = %s WHERE id = %s;"
        try:
            failed_missions = self.get_agent_by_id(id)["failed_missions"]
            failed_missions += 1
            cursor.execute(sql, (failed_missions, id))
            conn.commit()
            rowcount = cursor.rowcount
            return rowcount > 0
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        total = agent["completed_missions"] + agent["failed_missions"]
        dicti = {
            "total": total,
            "failed": agent["failed_missions"],
            "completed": agent["completed_missions"],
            "success_rate": round((agent["completed_missions"]/total) * 100, 2)
        }
        return dicti
    



connection_db = DbConnection()
if __name__ == "__main__":
    age_manager = AgentDB(connection_db)
    data1 = {"name": "Moshe", "specialty": "tech", "agent_rank": "Junior"}
    # print(age_manager.create_agent(data1))

    print(age_manager.get_all_agents())
    print(age_manager.increment_failed(1))

    print(age_manager.increment_completed(1))
    print(age_manager.get_agent_by_id(1))
    print(age_manager.get_agent_performance(1))