import json
import os

PROJECT_ROOT = os.path.dirname(__file__)

HEURISTIC_LOG = os.path.join(PROJECT_ROOT, "spades_heuristic_data", "spades_logs.jsonl")
MINIMAX_LOG   = os.path.join(PROJECT_ROOT, "spades_minimax_data", "spades_logs.jsonl")


def summarize_log(path):
    games = 0
    wins = 0
    losses = 0
    draws = 0
    total_margin = 0

    with open(path, encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            if event.get("event") != "hand_end":
                continue

            games += 1

            totals = event["totals"]  # [team0, team1]
            margin = totals[0] - totals[1]
            total_margin += margin

            if margin > 0:
                wins += 1
            elif margin < 0:
                losses += 1
            else:
                draws += 1

    avg_margin = total_margin / games if games > 0 else 0.0

    return {
        "games": games,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": wins / games if games > 0 else 0.0,
        "avg_margin": avg_margin,
    }


def pretty_print(name, stats):
    print(f"=== {name} ===")
    print(f"Games:      {stats['games']}")
    print(f"Wins:       {stats['wins']}")
    print(f"Losses:     {stats['losses']}")
    print(f"Draws:      {stats['draws']}")
    print(f"Win rate:   {stats['win_rate']:.3f}")
    print(f"Avg margin: {stats['avg_margin']:.3f}")
    print()


if __name__ == "__main__":
    print("Heuristic log path:", HEURISTIC_LOG)
    print("Minimax log path:", MINIMAX_LOG)

    heuristic_stats = summarize_log(HEURISTIC_LOG)
    minimax_stats = summarize_log(MINIMAX_LOG)

    pretty_print("Heuristic AI (seat 0)", heuristic_stats)
    pretty_print("Minimax AI (seat 0)", minimax_stats)

    print("=== Comparison ===")
    print(f"Win rate diff (minimax - heuristic): "
          f"{minimax_stats['win_rate'] - heuristic_stats['win_rate']:.3f}")
    print(f"Avg margin diff (minimax - heuristic): "
          f"{minimax_stats['avg_margin'] - heuristic_stats['avg_margin']:.3f}")
