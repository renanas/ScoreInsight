from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from config.db_setup import Base

# Modelo para a tabela Tournament_Club_Resume
class TournamentClubResume(Base):
    __tablename__ = 'tournament_club_resume'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    matches_played = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    assists = Column(Integer)

# Modelo para a tabela Tournament_Club_Resume_Attack
class TournamentClubResumeAttack(Base):
    __tablename__ = 'tournament_club_resume_attack'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    goals_per_match = Column(Float)
    penalty_goals = Column(Integer)
    free_kick_goals = Column(Integer)
    inside_box_goals = Column(Integer)
    outside_box_goals = Column(Integer)
    left_foot_goals = Column(Integer)
    right_foot_goals = Column(Integer)
    header_goals = Column(Integer)
    big_chances_per_match = Column(Float)
    big_chances_missed_per_match = Column(Float)
    total_shots_per_match = Column(Float)
    shots_on_target_per_match = Column(Float)
    shots_off_target_per_match = Column(Float)
    blocked_shots_per_match = Column(Float)
    dribbles_per_match = Column(Float)
    corners_per_match = Column(Float)
    fouls_per_match = Column(Float)
    shots_hit_woodwork = Column(Integer)
    counter_attacks = Column(Integer)

# Modelo para a tabela Tournament_Club_Resume_Pass
class TournamentClubResumePass(Base):
    __tablename__ = 'tournament_club_resume_pass'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    possession = Column(Float)
    accurate_passes = Column(Integer)
    accurate_passes_own_half = Column(Integer)
    accurate_passes_final_third = Column(Integer)
    long_balls = Column(Integer)
    accurate_crosses = Column(Integer)

# Modelo para a tabela Tournament_Club_Resume_Defending
class TournamentClubResumeDefending(Base):
    __tablename__ = 'tournament_club_resume_defending'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    clean_sheets = Column(Integer)
    goals_conceded_per_match = Column(Float)
    tackles_per_match = Column(Float)
    interceptions = Column(Integer)
    clearances = Column(Integer)
    saves_per_match = Column(Float)
    ball_recoveries_per_match = Column(Float)
    errors_leading_to_shot = Column(Integer)
    errors_leading_to_goal = Column(Integer)
    penalties_committed = Column(Integer)
    penalty_goals_conceded = Column(Integer)
    goal_line_clearances = Column(Integer)
    last_man_tackles = Column(Integer)

# Modelo para a tabela Tournament_Club_Resume_Others
class TournamentClubResumeOthers(Base):
    __tablename__ = 'tournament_club_resume_others'

    club_id = Column(Integer, ForeignKey('club.id'), primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    tackles_per_match = Column(Float)
    ground_duels_won = Column(Float)
    aerial_duels_won = Column(Float)
    possession_lost_per_match = Column(Float)
    throw_ins_per_match = Column(Float)
    goal_kicks_per_match = Column(Float)
    offsides_per_match = Column(Float)
    fouls_per_match = Column(Float)
    yellow_cards_per_match = Column(Float)
    red_cards = Column(Integer)