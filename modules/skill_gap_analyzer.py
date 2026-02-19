from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_skill_gap(resume_skills, role_skills):
    """
    Performs skill gap analysis using TF-IDF and Cosine Similarity
    """

    # Convert skill lists to strings
    resume_text = " ".join(resume_skills)
    role_text = " ".join(role_skills)

    documents = [resume_text, role_text]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Cosine Similarity
    similarity_score = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:2]
    )[0][0]

    match_percentage = int(similarity_score * 100)

    # Skill comparison (set-based for clarity)
    resume_set = set(resume_skills)
    role_set = set(role_skills)

    matched_skills = list(resume_set.intersection(role_set))
    missing_skills = list(role_set - resume_set)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }
