from logic.scoring import recommend

def run():
    role = input("Enter your role [top, jgl, mid, bot, supp]: ").upper()
    enemies = input("Enter enemy champions (comma separated): ").split(",")
    enemies = [e.strip().lower() for e in enemies]

    print("\n--- RESULTS ---\n")

    result = recommend(enemies, role)

    lane_enemy = result["lane_opponent"]

    if lane_enemy:
        print(f"Your most probable lane opponent: {lane_enemy.capitalize()}\n")
    else:
        print("No clear lane opponent detected\n")

    print("Best picks:\n")

    for champ, score in result["recommendations"]:
        print(f"{champ.capitalize():<15} | Score: {score:.2f}")