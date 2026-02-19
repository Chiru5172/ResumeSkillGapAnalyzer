import os
from flask import Flask, render_template, request, redirect, url_for
from database.db import get_db_connection
from modules.resume_parser import extract_resume_text
from modules.text_preprocessing import clean_text
from modules.skill_extractor import extract_skills_from_text
from modules.role_skill_fetcher import fetch_required_skills
from modules.skill_gap_analyzer import analyze_skill_gap
from modules.roadmap_generator import generate_roadmap

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    job_role = request.form.get("job_role")
    resume_file = request.files.get("resume")

    if not resume_file or resume_file.filename == "":
        return "No resume uploaded", 400

    if not allowed_file(resume_file.filename):
        return "Invalid file type", 400

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(file_path)

    # ===== NLP PIPELINE =====
    raw_text = extract_resume_text(file_path)
    cleaned_text = clean_text(raw_text)

    extracted_skills = extract_skills_from_text(cleaned_text)
    required_skills = fetch_required_skills(job_role)

    gap_result = analyze_skill_gap(extracted_skills, required_skills)
    matched_skills = gap_result["matched_skills"]
    missing_skills = gap_result["missing_skills"]
    match_percentage = gap_result["match_percentage"]

    # ===== DATABASE OPERATIONS =====
    conn = get_db_connection()
    cursor = conn.cursor()

    # User
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("Demo User", "demo@example.com")
    )
    user_id = cursor.lastrowid

    # Resume
    cursor.execute(
        "INSERT INTO resumes (user_id, file_name, job_role) VALUES (%s, %s, %s)",
        (user_id, resume_file.filename, job_role)
    )
    resume_id = cursor.lastrowid

    # Extracted skills
    for skill in extracted_skills:
        cursor.execute(
            "INSERT INTO extracted_skills (resume_id, skill_name) VALUES (%s, %s)",
            (resume_id, skill)
        )

    # Role required skills
    priority = 1
    for skill in required_skills:
        cursor.execute(
            "INSERT INTO role_required_skills (resume_id, skill_name, priority) VALUES (%s, %s, %s)",
            (resume_id, skill, priority)
        )
        priority += 1

    # Skill gap result
    cursor.execute(
        """
        INSERT INTO skill_gap_results
        (resume_id, matched_skills, missing_skills, match_percentage)
        VALUES (%s, %s, %s, %s)
        """,
        (
            resume_id,
            ", ".join(matched_skills),
            ", ".join(missing_skills),
            match_percentage
        )
    )

    # ===== ROADMAP =====
    roadmap = generate_roadmap(missing_skills)

    for item in roadmap:
        cursor.execute(
            """
            INSERT INTO roadmaps
            (resume_id, step_no, skill, project, certification, duration)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                resume_id,
                item["step"],
                item["skill"],
                item["project"],
                item["certification"],
                item["duration"]
            )
        )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard", resume_id=resume_id))


@app.route("/dashboard/<int:resume_id>")
def dashboard(resume_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT skill_name FROM extracted_skills WHERE resume_id=%s", (resume_id,))
    extracted_skills = [row[0] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT skill_name FROM role_required_skills WHERE resume_id=%s ORDER BY priority",
        (resume_id,)
    )
    required_skills = [row[0] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT matched_skills, missing_skills, match_percentage FROM skill_gap_results WHERE resume_id=%s",
        (resume_id,)
    )
    gap = cursor.fetchone()
    matched_skills = gap[0].split(", ") if gap else []
    missing_skills = gap[1].split(", ") if gap else []
    match_percentage = gap[2] if gap else 0

    cursor.execute(
        "SELECT step_no, skill, project, certification, duration FROM roadmaps WHERE resume_id=%s ORDER BY step_no",
        (resume_id,)
    )
    roadmap = cursor.fetchall()

    conn.close()
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    extracted_count = len(extracted_skills)
    required_count = len(required_skills)

    return render_template(
    "dashboard.html",
    resume_id=resume_id,
    skills=extracted_skills,
    required_skills=required_skills,
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    match_percentage=match_percentage,
    roadmap=roadmap,
    matched_count=matched_count,
    missing_count=missing_count,
    extracted_count=extracted_count,
    required_count=required_count
)

if __name__ == "__main__":
    app.run(debug=True)
