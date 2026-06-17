

# Intelligence Task Manager

### Description system:
Missions and agents management system




## Structure Folder

```
intelligence_task_manager/
|-- database/
|   |--db_connection.py
|   |--agent_db.py
|   |--mission.py
|--README.md
|--requirements.txt
|--.gitignore
```


## Tables

### Table 'agents'
The command to create the 'agents' table.
```commandline
CREATE TABLE IF NOT EXISTS agents (
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
specialty VARCHAR(50) NOT NULL,
is_active BOOLEAN DEFAULT TRUE,
completed_missions INT DEFAULT 0,
failed_missions INT DEFAULT 0,
agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
);
```


```
+--------------------+-------------------------------------+------+-----+---------+----------------+
| Field              | Type                                | Null | Key | Default | Extra          |
+--------------------+-------------------------------------+------+-----+---------+----------------+
| id                 | int                                 | NO   | PRI | NULL    | auto_increment |
| name               | varchar(50)                         | NO   |     | NULL    |                |
| specialty          | varchar(50)                         | NO   |     | NULL    |                |
| is_active          | tinyint(1)                          | YES  |     | 1       |                |
| completed_missions | int                                 | YES  |     | 0       |                |
| failed_missions    | int                                 | YES  |     | 0       |                |
| agent_rank         | enum('Junior','Senior','Commander') | NO   |     | NULL    |                |
+--------------------+-------------------------------------+------+-----+---------+----------------+

```

### Table 'missions'

The command to create the 'missions' table.
```commandline
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
```


```
+-------------------+-----------------------------------------------------------------------+------+-----+---------+----------------+
| Field             | Type                                                                  | Null | Key | Default | Extra          |
+-------------------+-----------------------------------------------------------------------+------+-----+---------+----------------+
| id                | int                                                                   | NO   | PRI | NULL    | auto_increment |
| title             | varchar(50)                                                           | NO   |     | NULL    |                |
| description       | text                                                                  | NO   |     | NULL    |                |
| location          | varchar(100)                                                          | YES  |     | NULL    |                |
| difficulty        | int                                                                   | NO   |     | NULL    |                |
| importance        | int                                                                   | NO   |     | NULL    |                |
| status            | enum('NEW','ASSIGNED','IN_PROGRESS','COMPLETED','FAILED','CANCELLED') | YES  |     | NEW     |                |
| risk_level        | enum('LOW','MEDIUM','HIGH','CRITICAL')                                | NO   |     | NULL    |                |
| assigned_agent_id | int                                                                   | YES  |     | NULL    |                |
+-------------------+-----------------------------------------------------------------------+------+-----+---------+----------------+
```


## System Rules
1. Rank must be ('Junior', 'Senior', 'Commander') otherwise exception will raise.
2. Difficulty and importance must be  between 1 and 10 otherwise exception.
3. Risk_level calculate automatically once the mission will be created.
4. An agent with is_active = False can't receive missions.
5. An agent can't hold mor than 3 open mission simultaneously.
6. Whether risk_level = CRITICAL - just an agent with Commander rank can receive the mission.
7. Can assign only mission with status 'NEW'. After that status = ASSIGNED.
8. Can start only mission with status ASSIGNED. After that status = IN_PROGRESS.
9. Can end only mission with status 'IN_PROGRESS', and change it to 'failed' or 'completed'.
10. Can cancel only mission with status NEW or ASSIGNED, otherwise exception.


# Installation

Clone the project from GitHub
```commandline
git clone https://github.com/emg4706-Elazar/Intelligence_Task_Manager.git
```


### Docker Setup

create a new container with database 'intelligence_db'
```commandline
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
-e MYSQL_DATABASE=intelligence_db -p 3306:3306 mysql:8.0
```


### Install the dependents packages
```commandline
cd ['Enter path']/Intelligence_Task_manager
```


```commandline
python -m pip install -r requirements.txt
```



### Running the server

```commandline
uvicorn main:app --reload
```