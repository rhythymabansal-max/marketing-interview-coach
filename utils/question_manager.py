
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTION_PATH = BASE_DIR / "data" / "question_bank.csv"

CATEGORIES = ["Marketing Fundamentals", "Digital Marketing", "Sales", "Marketing Analytics", "Brand Management", "HR/Behavioral", "Case/Scenario"]
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]
MODES = ["Quick Quiz", "Mock Interview", "Practice by Topic"]

def load_questions():
    df = pd.read_csv(QUESTION_PATH)
    required = {"id", "category", "difficulty", "question", "ideal_points"}
    if not required.issubset(df.columns):
        raise ValueError("Question bank is missing required columns.")
    return df

def select_questions(df, category, difficulty, mode, count, seed=42):
    if category not in CATEGORIES or difficulty not in DIFFICULTIES or mode not in MODES:
        raise ValueError("Invalid interview configuration.")
    if mode == "Practice by Topic":
        pool = df[(df.category == category) & (df.difficulty == difficulty)]
        if len(pool) < count:
            pool = df[df.category == category]
    elif mode == "Mock Interview":
        pool = df[df.difficulty == difficulty]
        if len(pool) < count:
            pool = df
    else:
        pool = df[(df.category == category) & (df.difficulty == difficulty)]
        if len(pool) < count:
            pool = df[df.category == category]
    if len(pool) < count:
        count = len(pool)
    return pool.sample(n=count, random_state=seed).reset_index(drop=True)
