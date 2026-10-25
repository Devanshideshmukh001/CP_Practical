"""Final Mini Project: Chemical Batch Quality Analysis

This project combines the main ideas from the course:
- batch ID validation using digits and loops
- exception handling for invalid input
- file I/O with CSV and JSON
- basic statistics
- data visualization
- simple chemical engineering decision making
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


CSV_FILE = Path("chemical_batch_data.csv")
JSON_FILE = Path("chemical_batch_summary.json")


def validate_batch_id(batch_id: str) -> dict:
    """Return a validation report for a chemical batch identifier."""
    if not isinstance(batch_id, str):
        raise TypeError("Batch ID must be a string.")

    if batch_id == "":
        raise ValueError("Batch ID cannot be empty.")

    if not batch_id.isdigit():
        raise ValueError(f"Batch ID '{batch_id}' must contain only digits.")

    if len(batch_id) != 8:
        raise ValueError(f"Batch ID '{batch_id}' must have exactly 8 digits.")

    digit_sum = sum(int(digit) for digit in batch_id)
    checksum = digit_sum % 10

    return {
        "batch_id": batch_id,
        "digit_sum": digit_sum,
        "checksum": checksum,
        "valid": True,
    }


def calculate_quality_score(purity: float, yield_pct: float, impurity_ppm: float, ph: float) -> float:
    """Create a simple quality score from the main plant quality indicators."""
    score = 0.50 * purity + 0.35 * yield_pct - 0.03 * impurity_ppm - 4 * abs(ph - 7.0)
    return round(score, 2)


def grade_batch(score: float) -> str:
    """Convert a numeric quality score into a letter grade."""
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    return "D"


def build_batch_dataframe() -> pd.DataFrame:
    """Create sample chemical batch data for the mini project."""
    records = [
        {
            "batch_id": "20260815",
            "product": "Methanol",
            "purity": 96.5,
            "yield_pct": 91.2,
            "impurity_ppm": 120,
            "ph": 7.1,
            "temperature_c": 62.4,
            "reaction_time_h": 3.2,
        },
        {
            "batch_id": "24073105",
            "product": "Ethanol",
            "purity": 93.8,
            "yield_pct": 88.7,
            "impurity_ppm": 150,
            "ph": 7.3,
            "temperature_c": 68.0,
            "reaction_time_h": 3.8,
        },
        {
            "batch_id": "31420688",
            "product": "Acetone",
            "purity": 98.1,
            "yield_pct": 94.5,
            "impurity_ppm": 90,
            "ph": 6.9,
            "temperature_c": 60.2,
            "reaction_time_h": 2.9,
        },
        {
            "batch_id": "40981234",
            "product": "Ammonia",
            "purity": 90.4,
            "yield_pct": 85.6,
            "impurity_ppm": 210,
            "ph": 7.7,
            "temperature_c": 59.5,
            "reaction_time_h": 4.1,
        },
        {
            "batch_id": "55678421",
            "product": "Acetic Acid",
            "purity": 95.2,
            "yield_pct": 90.8,
            "impurity_ppm": 135,
            "ph": 7.0,
            "temperature_c": 65.3,
            "reaction_time_h": 3.5,
        },
        {
            "batch_id": "60194328",
            "product": "Benzene",
            "purity": 92.7,
            "yield_pct": 87.9,
            "impurity_ppm": 180,
            "ph": 7.5,
            "temperature_c": 71.1,
            "reaction_time_h": 4.0,
        },
    ]

    df = pd.DataFrame(records)
    df["digit_sum"] = df["batch_id"].apply(lambda batch_id: sum(int(digit) for digit in batch_id))
    df["quality_score"] = df.apply(
        lambda row: calculate_quality_score(
            row["purity"],
            row["yield_pct"],
            row["impurity_ppm"],
            row["ph"],
        ),
        axis=1,
    )
    df["grade"] = df["quality_score"].apply(grade_batch)
    return df


def save_batch_data(df: pd.DataFrame) -> None:
    """Save processed batch data to CSV and summary to JSON."""
    df.to_csv(CSV_FILE, index=False)

    summary = {
        "average_purity": round(df["purity"].mean(), 2),
        "average_yield": round(df["yield_pct"].mean(), 2),
        "average_quality_score": round(df["quality_score"].mean(), 2),
        "best_batch": df.loc[df["quality_score"].idxmax(), "batch_id"],
        "grade_counts": df["grade"].value_counts().to_dict(),
    }

    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"Saved batch data to {CSV_FILE}")
    print(f"Saved summary to {JSON_FILE}")


def analyze_and_report(df: pd.DataFrame) -> dict:
    """Return a short summary statistic dictionary and print it."""
    summary = {
        "total_batches": len(df),
        "average_purity": round(df["purity"].mean(), 2),
        "average_yield": round(df["yield_pct"].mean(), 2),
        "average_quality_score": round(df["quality_score"].mean(), 2),
        "best_grade": df["grade"].mode().iloc[0],
    }

    print("\nChemical Batch Quality Report")
    print("-" * 30)
    print(f"Total batches: {summary['total_batches']}")
    print(f"Average purity: {summary['average_purity']}%")
    print(f"Average yield: {summary['average_yield']}%")
    print(f"Average quality score: {summary['average_quality_score']}")
    print(f"Most common grade: {summary['best_grade']}")

    return summary


def plot_quality_results(df: pd.DataFrame) -> None:
    """Plot batch quality scores using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df["batch_id"], df["quality_score"], color=["#2E86DE" if score >= 70 else "#F39C12" for score in df["quality_score"]])
    ax.set_title("Chemical Batch Quality Score")
    ax.set_xlabel("Batch ID")
    ax.set_ylabel("Quality Score")
    ax.axhline(70, color="red", linestyle="--", linewidth=1.2, label="Pass threshold")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Run the final chemical batch project."""
    try:
        df = build_batch_dataframe()

        for batch_id in df["batch_id"]:
            validation = validate_batch_id(batch_id)
            print(f"Batch {validation['batch_id']} validated: digit sum = {validation['digit_sum']}, checksum = {validation['checksum']}")

        print("\nBatch quality grades:")
        print(df[["batch_id", "product", "quality_score", "grade"]].to_string(index=False))

        analyze_and_report(df)
        save_batch_data(df)
        plot_quality_results(df)

    except (TypeError, ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
