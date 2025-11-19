

import csv
import ast
import argparse
from collections import defaultdict


def make_state_key(row):
    initial_hand = ast.literal_eval(row['initial_hand'])
    dealer_up = int(row['dealer_up'])
    true_count = int(row['true_count'])
    total = sum(initial_hand)
    is_soft = 11 in initial_hand
    return (total, bool(is_soft), dealer_up, true_count)


def first_action(row):
    actions_str = row['actions_taken']
    if not actions_str:
        return None
    actions_nested = ast.literal_eval(actions_str)
    if not actions_nested or not actions_nested[0]:
        return None
    return actions_nested[0][0]


def build_V_and_Q(csv_path):
    V_sum = defaultdict(float)
    V_n = defaultdict(int)
    Q_sum = defaultdict(float)
    Q_n = defaultdict(int)

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            win_str = row.get('win', '')
            if win_str is None or win_str == '':
                continue
            try:
                G = float(win_str)
            except ValueError:
                continue
            try:
                s = make_state_key(row)
            except Exception as e:
                print(f"Warning: skipping row due to state parse error: {e}")
                continue
            V_sum[s] += G
            V_n[s] += 1
            try:
                a = first_action(row)
            except Exception as e:
                print(f"Warning: skipping action for row due to parse error: {e}")
                a = None
            if a is not None:
                Q_sum[(s, a)] += G
                Q_n[(s, a)] += 1

    V = {s: V_sum[s] / V_n[s] for s in V_sum}
    Q = {(s, a): Q_sum[(s, a)] / Q_n[(s, a)] for (s, a) in Q_sum}
    return V, Q, V_n, Q_n


def summarize_V(V, V_n, k=10):
    if not V:
        print("No V(s) entries built.")
        return
    items = sorted(V.items(), key=lambda x: x[1])
    print("\n=== Worst states by V(s) ===")
    for s, v in items[:k]:
        print(f"State {s} -> EV {v:.3f} (samples: {V_n[s]})")
    print("\n=== Best states by V(s) ===")
    for s, v in items[-k:]:
        print(f"State {s} -> EV {v:.3f} (samples: {V_n[s]})")


def summarize_Q(Q, Q_n, k=10):
    if not Q:
        print("No Q(s,a) entries built.")
        return
    items = sorted(Q.items(), key=lambda x: x[1])
    print("\n=== Worst (state, action) by Q(s,a) ===")
    for (s, a), q in items[:k]:
        print(f"State {s}, action {a} -> EV {q:.3f} (samples: {Q_n[(s, a)]})")
    print("\n=== Best (state, action) by Q(s,a) ===")
    for (s, a), q in items[-k:]:
        print(f"State {s}, action {a} -> EV {q:.3f} (samples: {Q_n[(s, a)]})")


def save_V_csv(V, V_n, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["player_total", "is_soft", "dealer_up", "true_count", "EV", "samples"])
        for (total, is_soft, dealer_up, true_count), ev in V.items():
            ev = round(ev, 3)
            samples = V_n[(total, is_soft, dealer_up, true_count)]
            writer.writerow([total, is_soft, dealer_up, true_count, ev, samples])


def save_Q_csv(Q, Q_n, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["player_total", "is_soft", "dealer_up", "true_count", "action", "EV", "samples"])
        for (s, a), ev in Q.items():
            total, is_soft, dealer_up, true_count = s
            ev = round(ev, 3)
            samples = Q_n[(s, a)]
            writer.writerow([total, is_soft, dealer_up, true_count, a, ev, samples])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='blackjack_dev.csv',
                        help='Path to blackjack simulator CSV file')
    args = parser.parse_args()

    print(f"Reading data from: {args.input}")
    V, Q, V_n, Q_n = build_V_and_Q(args.input)

    print(f"\nBuilt V(s) for {len(V)} distinct states.")
    print(f"Built Q(s,a) for {len(Q)} distinct (state, action) pairs.")

    summarize_V(V, V_n)
    summarize_Q(Q, Q_n)

    print("\nSaving full V(s) table to V_full.csv...")
    save_V_csv(V, V_n, "V_full.csv")

    print("Saving full Q(s,a) table to Q_full.csv...")
    save_Q_csv(Q, Q_n, "Q_full.csv")

    print("\nDone.")


if __name__ == '__main__':
    main()
