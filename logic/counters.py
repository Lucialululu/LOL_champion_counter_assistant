import pandas as pd

df = pd.read_csv("data/matchups_aggregated_1000.csv")

def get_lane_counters(enemy, role, top_n=5, min_games=5):
    enemy = enemy.lower()
    role = role.upper()
    
    subset = df[(df["opponent"] == enemy) & (df["role"] == role) & (df["games"] >= min_games)].copy()
    
    if subset.empty:
        subset = df[df["opponent"] == enemy].copy()
    
    subset["score"] = subset["winrate"] * (subset["games"] ** 0.5)
    
    return subset.sort_values(["score", "games"], ascending=False).head(top_n)

def get_team_counters(enemies, role, top_n=5, min_games=5):
    scores = {}
    
    role = role.upper()
    
    for enemy in enemies:
        enemy = enemy.lower()
        
        subset = df[(df["opponent"] == enemy) & (df["role"] == role) & (df["games"] >= min_games)].copy()
        
        if subset.empty:
            subset = df[df["opponent"] == enemy]
        
        for champ, winrate, games in zip(
            subset["champion"],
            subset["winrate"],
            subset["games"]
        ):
            score = (winrate - 0.5) * (games ** 0.5)
            scores[champ] = scores.get(champ, 0) + score
    
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    return [{"champion": k, "score": v} for k, v in top]

