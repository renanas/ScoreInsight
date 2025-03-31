def create_tables(connectionDB):
    """
    Cria as tabelas no banco de dados PostgreSQL.
    """
    commands = [
        # Adicione o comando SQL para criar a tabela treinador na lista de comandos
        """
        CREATE TABLE IF NOT EXISTS coach (
            id SERIAL PRIMARY KEY,               
            id_sofascore INTEGER NOT NULL,       
            name TEXT NOT NULL,                  
            nationality TEXT,                    
            games_played INTEGER,
            performance TEXT,                
            points INTEGER                       
        )
        """,
        # Tabela Club
        """
        CREATE TABLE IF NOT EXISTS club (
            id SERIAL PRIMARY KEY,
            id_sofascore INTEGER NOT NULL,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT,
            date_foundation DATE,
            coach INTEGER, 
            stadium TEXT,
            xpath TEXT,
            FOREIGN KEY (coach) REFERENCES coach (id) 
        )
        """,        
        # Tabela Tournament
        """
        CREATE TABLE IF NOT EXISTS tournament (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
        """,
        # Tabela Tournament_Club
        """
        CREATE TABLE IF NOT EXISTS tournament_club (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            position INTEGER,
            games_played INTEGER,
            wins INTEGER,
            draws INTEGER,
            losses INTEGER,
            goals_scored INTEGER,
            goals_conceded INTEGER,
            points INTEGER,
            last_games TEXT,
            season TEXT,
            PRIMARY KEY (club_id, tournament_id, season),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Home
        """
        CREATE TABLE IF NOT EXISTS tournament_club_home (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            position INTEGER,
            games_played INTEGER,
            wins INTEGER,
            draws INTEGER,
            losses INTEGER,
            goals_scored INTEGER,
            goals_conceded INTEGER,
            points INTEGER,
            last_games TEXT,
            season TEXT,
            PRIMARY KEY (club_id, tournament_id, season),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Visiting
        """
        CREATE TABLE IF NOT EXISTS tournament_club_visiting (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            position INTEGER,
            games_played INTEGER,
            wins INTEGER,
            draws INTEGER,
            losses INTEGER,
            goals_scored INTEGER,
            goals_conceded INTEGER,
            points INTEGER,
            last_games TEXT,
            season TEXT,
            PRIMARY KEY (club_id, tournament_id, season),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Resume
        """
        CREATE TABLE IF NOT EXISTS tournament_club_resume (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            matches_played INTEGER,
            goals_scored INTEGER,
            goals_conceded INTEGER,
            assists INTEGER,
            PRIMARY KEY (club_id, tournament_id),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Resume_Attack
        """
        CREATE TABLE IF NOT EXISTS tournament_club_resume_attack (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            goals_per_match REAL,
            penalty_goals INTEGER,
            free_kick_goals INTEGER,
            inside_box_goals INTEGER,
            outside_box_goals INTEGER,
            left_foot_goals INTEGER,
            right_foot_goals INTEGER,
            header_goals INTEGER,
            big_chances_per_match REAL,
            big_chances_missed_per_match REAL,
            total_shots_per_match REAL,
            shots_on_target_per_match REAL,
            shots_off_target_per_match REAL,
            blocked_shots_per_match REAL,
            dribbles_per_match REAL,
            corners_per_match REAL,
            fouls_per_match REAL,
            shots_hit_woodwork INTEGER,
            counter_attacks INTEGER,
            PRIMARY KEY (club_id, tournament_id),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Resume_Pass
        """
        CREATE TABLE IF NOT EXISTS tournament_club_resume_pass (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            possession REAL,
            accurate_passes INTEGER,
            accurate_passes_own_half INTEGER,
            accurate_passes_final_third INTEGER,
            long_balls INTEGER,
            accurate_crosses INTEGER,
            PRIMARY KEY (club_id, tournament_id),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Resume_Defending
        """
        CREATE TABLE IF NOT EXISTS tournament_club_resume_defending (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            clean_sheets INTEGER,
            goals_conceded_per_match REAL,
            tackles_per_match REAL,
            interceptions INTEGER,
            clearances INTEGER,
            saves_per_match REAL,
            ball_recoveries_per_match REAL,
            errors_leading_to_shot INTEGER,
            errors_leading_to_goal INTEGER,
            penalties_committed INTEGER,
            penalty_goals_conceded INTEGER,
            goal_line_clearances INTEGER,
            last_man_tackles INTEGER,
            PRIMARY KEY (club_id, tournament_id),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """,
        # Tabela Tournament_Club_Resume_Others
        """
        CREATE TABLE IF NOT EXISTS tournament_club_resume_others (
            club_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            tackles_per_match REAL,
            ground_duels_won REAL,
            aerial_duels_won REAL,
            possession_lost_per_match REAL,
            throw_ins_per_match REAL,
            goal_kicks_per_match REAL,
            offsides_per_match REAL,
            fouls_per_match REAL,
            yellow_cards_per_match REAL,
            red_cards INTEGER,
            PRIMARY KEY (club_id, tournament_id),
            FOREIGN KEY (club_id) REFERENCES club (id),
            FOREIGN KEY (tournament_id) REFERENCES tournament (id)
        )
        """
    ]

    if connectionDB:
        try:
            cursor = connectionDB.cursor()
            for command in commands:
                cursor.execute(command)
            connectionDB.commit()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            cursor.close()
            connectionDB.close()

if __name__ == "__main__":
    create_tables()