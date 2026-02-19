-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RESUMES TABLE
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    file_name VARCHAR(255),
    job_role VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- EXTRACTED SKILLS
CREATE TABLE extracted_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    skill_name VARCHAR(100),
    FOREIGN KEY (resume_id) REFERENCES resumes(id)
);

-- SKILL GAP RESULTS
CREATE TABLE skill_gap_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    matched_skills TEXT,
    missing_skills TEXT,
    match_percentage INT,
    FOREIGN KEY (resume_id) REFERENCES resumes(id)
);

-- ROADMAP TABLE
CREATE TABLE roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    step_no INT,
    skill VARCHAR(100),
    project VARCHAR(255),
    certification VARCHAR(255),
    duration VARCHAR(50),
    FOREIGN KEY (resume_id) REFERENCES resumes(id)
);

CREATE TABLE role_required_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    skill_name VARCHAR(100),
    priority INT,
    FOREIGN KEY (resume_id) REFERENCES resumes(id)
);
