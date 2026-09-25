from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path

app = FastAPI(title="Students API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).with_name("students.csv")

with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as f:
    students = [
        {"studentId": int(row["studentId"]), "class": row["class"]}
        for row in csv.DictReader(f)
    ]


@app.get("/api")
async def get_students(class_names: list[str] = Query(default=[], alias="class")):
    if not class_names:
        return {"students": students}

    requested = set(class_names)
    return {
        "students": [
            student for student in students
            if student["class"] in requested
        ]
    }
