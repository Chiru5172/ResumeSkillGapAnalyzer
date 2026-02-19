import os

# Load skills from file
def load_skills():
    skill_file = os.path.join("data", "skills_master.txt")
    with open(skill_file, "r", encoding="utf-8") as f:
        skills = [line.strip().lower() for line in f.readlines()]
    return skills


def extract_skills_from_text(cleaned_text):
    skills_list = load_skills()
    extracted_skills = set()

    for skill in skills_list:
        # phrase-level matching
        if skill in cleaned_text:
            extracted_skills.add(skill)

    return list(extracted_skills)
