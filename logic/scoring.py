import pandas as pd

# Load dataset
df = pd.read_csv("data/matchups_aggregated_1000.csv")

df["champion"] = df["champion"].str.lower()
df["opponent"] = df["opponent"].str.lower()
df["role"] = df["role"].str.upper()
df["role"] = df["role"].replace({"BOTTOM": "BOT", "SUPPORT": "SUPP", "MIDDLE": "MID", "TOP": "TOP", "JUNGLE": "JGL"})

def build_role_map(df):
    role_counts = (
        df.groupby(["champion", "role"])["games"]
        .sum()
        .reset_index()
    )
    
    main_roles = (
        role_counts.sort_values("games", ascending=False)
        .drop_duplicates("champion")
    )
    
    return dict(zip(main_roles["champion"], main_roles["role"]))


ROLE_MAP = build_role_map(df)


def find_lane_opponent(enemies, role):
    role = role.upper()
    
    candidates = [champ.lower() for champ in enemies if ROLE_MAP.get(champ.lower()) == role]
    
    if len(candidates) == 1:
        return candidates[0]
    
    if len(candidates) > 1:
        return candidates[0]
    
    return None

def compute_score(winrate, games):
    # Better than raw winrate
    return (winrate - 0.5) * (games ** 0.5)

def score_lane(df, enemy, role, min_games=5):
    enemy = enemy.lower()
    role = role.upper()
    
    subset = df[
        (df["opponent"] == enemy) &
        (df["role"] == role) &
        (df["games"] >= min_games)
    ].copy()
    
    if subset.empty:
        subset = df[df["opponent"] == enemy].copy()
    
    subset["score"] = compute_score(subset["winrate"], subset["games"])
    
    return subset

def score_team(df, enemies, role, min_games=5):
    role = role.upper()
    scores = {}
    
    for enemy in enemies:
        enemy = enemy.lower()
        
        subset = df[
            (df["opponent"] == enemy) &
            (df["role"] == role) &
            (df["games"] >= min_games)
        ]
        
        if subset.empty:
            subset = df[df["opponent"] == enemy]
        
        for champ, winrate, games in zip(
            subset["champion"],
            subset["winrate"],
            subset["games"]
        ):
            score = compute_score(winrate, games)
            scores[champ] = scores.get(champ, 0) + score
    
    return scores

def recommend(enemies, role, top_n=5):
    enemies = [e.lower() for e in enemies]
    role = role.upper()
    
    lane_enemy = find_lane_opponent(enemies, role)
    
    team_scores = score_team(df, enemies, role)
    
    # if lane opponent exists we add a higher score
    if lane_enemy:
        lane_df = score_lane(df, lane_enemy, role)
        
        for _, row in lane_df.iterrows():
            champ = row["champion"]
            lane_score = row["score"]
            
            # weight lane higher
            team_scores[champ] = team_scores.get(champ, 0) + (lane_score * 2)
    
    # Sort final results
    ranked = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "lane_opponent": lane_enemy,
        "recommendations": ranked[:top_n]
    }