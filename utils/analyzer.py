import json
import re
from pathlib import Path
from typing import Dict, List, Set

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_PATH = BASE_DIR / "data" / "skills.json"
ROLES_PATH = BASE_DIR / "data" / "job_roles.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str, skills: List[str]) -> Set[str]:
    normalized = normalize_text(text)
    found = set()

    for skill in skills:
        skill_lower = skill.lower()
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"
        if re.search(pattern, normalized):
            found.add(skill)

    return found


def calculate_similarity(resume_text: str, job_description: str) -> float:
    documents = [resume_text, job_description]

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(documents)
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except ValueError:
        return 0.0


def recommend_roles(resume_skills: Set[str], role_data: Dict[str, List[str]]) -> List[str]:
    ranked_roles = []

    for role, required_skills in role_data.items():
        required_set = set(required_skills)
        if not required_set:
            continue

        match_count = len(resume_skills.intersection(required_set))
        score = match_count / len(required_set)

        if match_count > 0:
            ranked_roles.append((role, score, match_count))

    ranked_roles.sort(key=lambda item: (item[1], item[2]), reverse=True)
    return [role for role, _, _ in ranked_roles[:3]]


def build_suggestions(
    resume_text: str,
    resume_skills: Set[str],
    job_skills: Set[str],
    missing_skills: Set[str],
    word_count: int
) -> List[str]:
    suggestions = []
    normalized = normalize_text(resume_text)

    if word_count < 200:
        suggestions.append(
            "Add more relevant project, internship, achievement, and responsibility details."
        )
    elif word_count > 900:
        suggestions.append(
            "Reduce unnecessary content and keep the resume focused and concise."
        )

    if "project" not in normalized and "projects" not in normalized:
        suggestions.append("Add a Projects section with technologies and measurable results.")

    if "experience" not in normalized and "internship" not in normalized:
        suggestions.append("Add internship, training, volunteer, or practical experience.")

    if "education" not in normalized:
        suggestions.append("Add a clearly labelled Education section.")

    if not re.search(r"\b\d+%|\b\d+\+|\b\d+\b", resume_text):
        suggestions.append(
            "Use measurable achievements, such as percentages, rankings, users, or completion time."
        )

    if job_skills and missing_skills:
        important_missing = sorted(missing_skills)[:5]
        suggestions.append(
            "Learn or demonstrate these job-related skills: "
            + ", ".join(important_missing)
            + "."
        )

    if len(resume_skills) < 4:
        suggestions.append(
            "Add a clear Technical Skills section with tools, languages, databases, and frameworks."
        )

    suggestions.append(
        "Use action verbs such as developed, implemented, designed, improved, and collaborated."
    )
    suggestions.append(
        "Do not add skills you cannot explain or demonstrate during an interview."
    )

    return suggestions


def analyze_resume(resume_text: str, job_description: str) -> Dict:
    all_skills = load_json(SKILLS_PATH)
    role_data = load_json(ROLES_PATH)

    resume_skills = extract_skills(resume_text, all_skills)
    job_skills = extract_skills(job_description, all_skills)

    matching_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    similarity_score = calculate_similarity(resume_text, job_description)

    if job_skills:
        skill_match_score = round(
            len(matching_skills) / len(job_skills) * 100,
            2
        )
    else:
        skill_match_score = 0.0

    ats_score = round(
        (similarity_score * 0.55) + (skill_match_score * 0.45)
    )
    ats_score = max(0, min(100, ats_score))

    word_count = len(resume_text.split())

    suggestions = build_suggestions(
        resume_text,
        resume_skills,
        job_skills,
        missing_skills,
        word_count
    )

    recommended_roles = recommend_roles(resume_skills, role_data)

    return {
        "ats_score": ats_score,
        "similarity_score": similarity_score,
        "skill_match_score": skill_match_score,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "recommended_roles": recommended_roles,
        "suggestions": suggestions,
        "word_count": word_count
    }


def generate_text_report(result: Dict) -> str:
    lines = [
        "AI RESUME ANALYZER REPORT",
        "=" * 45,
        f"ATS Match Score: {result['ats_score']}%",
        f"Text Similarity Score: {result['similarity_score']}%",
        f"Skill Match Score: {result['skill_match_score']}%",
        f"Resume Word Count: {result['word_count']}",
        "",
        "Skills Found:",
        ", ".join(result["resume_skills"]) or "None",
        "",
        "Matching Skills:",
        ", ".join(result["matching_skills"]) or "None",
        "",
        "Missing Skills:",
        ", ".join(result["missing_skills"]) or "None",
        "",
        "Recommended Job Roles:",
    ]

    if result["recommended_roles"]:
        lines.extend(f"- {role}" for role in result["recommended_roles"])
    else:
        lines.append("- No role recommendation available")

    lines.extend(["", "Suggestions:"])
    lines.extend(f"- {suggestion}" for suggestion in result["suggestions"])

    lines.extend([
        "",
        "Disclaimer:",
        "This score is an educational estimate and not an official company ATS result."
    ])

    return "\n".join(lines)
