# Knowledge base for roadmap generation
ROADMAP_KB = {
    "python": {
        "project": "Build a data analysis script",
        "certification": "Python for Everybody (Coursera)",
        "duration": "2 weeks"
    },
    "sql": {
        "project": "Design a relational database",
        "certification": "SQL for Data Science",
        "duration": "2 weeks"
    },
    "statistics": {
        "project": "Statistical analysis on dataset",
        "certification": "Statistics for Data Science",
        "duration": "2 weeks"
    },
    "power bi": {
        "project": "Interactive business dashboard",
        "certification": "Microsoft Power BI Certification",
        "duration": "3 weeks"
    },
    "machine learning": {
        "project": "Build a prediction model",
        "certification": "Machine Learning by Andrew Ng",
        "duration": "4 weeks"
    },
    "react": {
        "project": "Develop a single-page application",
        "certification": "React Developer Certification",
        "duration": "3 weeks"
    },
    "tensorflow": {
        "project": "Neural network for image classification",
        "certification": "TensorFlow Developer Certificate",
        "duration": "4 weeks"
    }
}

def generate_roadmap(missing_skills):
    roadmap = []
    step = 1

    for skill in missing_skills:
        skill = skill.lower()

        if skill in ROADMAP_KB:
            data = ROADMAP_KB[skill]
        else:
            # Default fallback
            data = {
                "project": f"Mini project using {skill}",
                "certification": f"Online course on {skill}",
                "duration": "2 weeks"
            }

        roadmap.append({
            "step": step,
            "skill": skill,
            "project": data["project"],
            "certification": data["certification"],
            "duration": data["duration"]
        })

        step += 1

    return roadmap
