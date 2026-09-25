#!/usr/bin/env python3
"""
flake_tracker.py

Very simple demo of how you'd measure "flake rate trending down" over time.

A "flake" = a test that failed, then passed on an immediate rerun with
no code change. This script simulates a run history (as if pulled from
your CI API) and reports the flake rate per week.

In a real setup, `load_runs()` would call your CI provider's API
(GitHub Actions, CircleCI, Jenkins) instead of generating fake data.
"""
import random
from collections import defaultdict

random.seed(7)  # reproducible demo output


def load_runs():
    """
    Simulates 8 weeks of CI history.
    Each run: (week, test_name, failed_then_passed_on_rerun: bool)

    Flake rate is modeled as improving over time (0.18 -> 0.02) to
    represent the effect of the fixes: more resources, sane timeouts,
    idempotent-only retries, parallel + seeded tests.
    """
    weekly_flake_prob = [0.18, 0.16, 0.13, 0.10, 0.07, 0.05, 0.03, 0.02]
    runs_per_week = 200
    data = []
    for week, prob in enumerate(weekly_flake_prob, start=1):
        for _ in range(runs_per_week):
            data.append((week, random.random() < prob))
    return data


def flake_rate_by_week(runs):
    totals = defaultdict(int)
    flakes = defaultdict(int)
    for week, is_flake in runs:
        totals[week] += 1
        if is_flake:
            flakes[week] += 1
    return {
        week: round(100 * flakes[week] / totals[week], 1)
        for week in sorted(totals)
    }


def main():
    runs = load_runs()
    rates = flake_rate_by_week(runs)

    print("Week | Flake rate | Trend")
    print("-----|-----------|------")
    prev = None
    for week, rate in rates.items():
        if prev is None:
            trend = "  -"
        elif rate < prev:
            trend = "down"
        elif rate > prev:
            trend = " up"
        else:
            trend = "flat"
        print(f"  {week:>2} | {rate:>8}% | {trend}")
        prev = rate

    first, last = list(rates.values())[0], list(rates.values())[-1]
    print(f"\nFlake rate went from {first}% to {last}% "
          f"({round(first - last, 1)} pt reduction) after rolling out the fixes.")


if __name__ == "__main__":
    main()
