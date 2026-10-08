from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTION_PATH = BASE_DIR / "data" / "question_bank.csv"

CATEGORIES = [
    "Marketing Fundamentals",
    "Digital Marketing",
    "Sales",
    "Marketing Analytics",
    "Brand Management",
    "HR/Behavioral",
    "Case/Scenario",
]

DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

MODES = ["Quick Quiz", "Mock Interview", "Practice by Topic"]


def load_questions():
    df = pd.read_csv(QUESTION_PATH)

    required = {"id", "category", "difficulty", "question", "ideal_points"}

    if not required.issubset(df.columns):
        raise ValueError("Question bank is missing required columns.")

    return df


def get_available_count(df, category, difficulty, mode):
    """Return the number of questions available for the selected configuration."""

    if category not in CATEGORIES:
        raise ValueError("Invalid interview category.")

    if difficulty not in DIFFICULTIES:
        raise ValueError("Invalid difficulty.")

    if mode not in MODES:
        raise ValueError("Invalid interview mode.")

    if mode == "Mock Interview":
        pool = df[df["difficulty"] == difficulty]
    else:
        pool = df[
            (df["category"] == category)
            & (df["difficulty"] == difficulty)
        ]

    return len(pool)


def select_questions(df, category, difficulty, mode, count, seed=42):
    """Select questions without changing the user's chosen difficulty."""

    if category not in CATEGORIES:
        raise ValueError("Invalid interview category.")

    if difficulty not in DIFFICULTIES:
        raise ValueError("Invalid difficulty.")

    if mode not in MODES:
        raise ValueError("Invalid interview mode.")

    if count < 1:
        raise ValueError("Number of questions must be at least 1.")

    if mode == "Mock Interview":
        pool = df[df["difficulty"] == difficulty]
    else:
        pool = df[
            (df["category"] == category)
            & (df["difficulty"] == difficulty)
        ]

    if pool.empty:
        raise ValueError(
            f"No questions are currently available for "
            f"{category} at {difficulty} difficulty."
        )

    if len(pool) < count:
        raise ValueError(
            f"Only {len(pool)} question(s) are available for "
            f"{category} at {difficulty} difficulty. "
            f"Please reduce the number of questions or choose another "
            f"category/difficulty."
        )

    return pool.sample(
        n=count,
        random_state=seed
    ).reset_index(drop=True)