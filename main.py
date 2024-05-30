import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        player_name TEXT NOT NULL,
        team_abbreviation TEXT NOT NULL,
        age INTEGER NOT NULL,
        player_height REAL NOT NULL,
        player_weight REAL NOT NULL,
        college TEXT,
        country TEXT,
        draft_year INTEGER,
        draft_round INTEGER,
        draft_number INTEGER
    )
''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY,
                    player_id INTEGER NOT NULL,
                    season TEXT NOT NULL,
                    gp INTEGER NOT NULL,
                    pts REAL NOT NULL,
                    reb REAL NOT NULL,
                    ast REAL NOT NULL,
                    net_rating REAL,
                    oreb_pct REAL,
                    dreb_pct REAL,
                    usg_pct REAL,
                    ts_pct REAL,
                    ast_pct REAL,
                    FOREIGN KEY(player_id) REFERENCES players(id)
                )
            ''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    # Метод для получения статистики игрока по его имени
    def get_player_stats_by_name(self, name):
        sql = '''
            SELECT player_name, season, gp, pts, reb, ast 
            FROM data 
            WHERE player_name = ?
        '''
        return self.__select_data(sql, (name,))
    
    def get_players_by_team(self, team_name):
        sql = '''
            SELECT * FROM data WHERE team_abbreviation = ? AND season = '2022-23'
            LIMIT 10
        '''
        return self.__select_data(sql, (team_name,))
    
    def get_player_data_by_name(self, name):
        sql = '''
            SELECT player_name, season, age, player_height, player_weight, college, country, draft_year, draft_number
            FROM data
            WHERE player_name = ?
        '''
        return self.__select_data(sql, (name,))
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()

