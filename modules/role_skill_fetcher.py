import requests
from config import ROLE_SKILL_API_KEY, ROLE_SKILL_API_URL


# 🔁 FALLBACK SKILLS (Used if API fails)
ROLE_SKILL_FALLBACK = {
    "data analyst": [
        "python", "sql", "statistics", "excel", "power bi", "data visualization"
    ],
    "web developer": [
        "html", "css", "javascript", "react", "git", "rest api"
    ],
    "machine learning engineer": [
        "python", "machine learning", "deep learning", "tensorflow", "statistics"
    ],
    "software engineer": [
        "java", "python", "data structures", "algorithms", "sql", "git"
    ]
}


def fetch_required_skills(job_role):
    """
    Fetch required skills for a given job role.
    Uses API if available, otherwise falls back to intelligent defaults.
    """

    # Normalize role
    normalized_role = job_role.lower().strip()

    # ---- TRY REAL API FIRST ----
    try:
        headers = {
            "Authorization": f"Bearer {ROLE_SKILL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": f"List key technical skills required for the role: {job_role}"
        }

        response = requests.post(
            ROLE_SKILL_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        skills = data.get("skills", [])
        skills = [skill.lower() for skill in skills]

        if skills:
            return skills

    except Exception as e:
        print("API ERROR (Falling back to local skill map):", e)

    # ---- FALLBACK LOGIC ----
    for role_key in ROLE_SKILL_FALLBACK:
        if role_key in normalized_role:
            return ROLE_SKILL_FALLBACK[role_key]

    # ---- DEFAULT FALLBACK ----
    return ["programming", "problem solving", "communication"]
