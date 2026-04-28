from typing import List, Dict
import re


class JobMatcher:
    def __init__(self):
        pass

    # ---------------------------
    # Basic Text Cleaning
    # ---------------------------
    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return text

    # ---------------------------
    # Extract Skills (simple version)
    # ---------------------------
    def extract_skills(self, text: str, skill_list: List[str]) -> List[str]:
        text = self.preprocess_text(text)
        found_skills = []

        for skill in skill_list:
            if skill.lower() in text:
                found_skills.append(skill.lower())

        return list(set(found_skills))

    # ---------------------------
    # Score a Single Job
    # ---------------------------
    def score_job(
        self,
        resume_text: str,
        job: Dict,
        skill_list: List[str]
    ) -> Dict:

        resume_text_clean = self.preprocess_text(resume_text)
        job_desc_clean = self.preprocess_text(job.get("description", ""))

        resume_skills = self.extract_skills(resume_text_clean, skill_list)
        job_skills = self.extract_skills(job_desc_clean, skill_list)

        # Skill overlap score
        matched_skills = list(set(resume_skills) & set(job_skills))
        skill_score = len(matched_skills)

        # Keyword frequency bonus
        keyword_score = 0
        for skill in job_skills:
            keyword_score += resume_text_clean.count(skill)

        total_score = skill_score * 2 + keyword_score

        return {
            "job_title": job.get("title"),
            "score": total_score,
            "matched_skills": matched_skills,
            "missing_skills": list(set(job_skills) - set(resume_skills)),
        }

    # ---------------------------
    # Rank Multiple Jobs
    # ---------------------------
    def rank_jobs(
        self,
        resume_text: str,
        jobs: List[Dict],
        skill_list: List[str]
    ) -> List[Dict]:

        scored_jobs = []

        for job in jobs:
            scored = self.score_job(resume_text, job, skill_list)
            scored_jobs.append(scored)

        # Sort descending by score
        ranked_jobs = sorted(
            scored_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_jobs


# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    matcher = JobMatcher()

    resume = """
    Python developer with experience in machine learning, APIs, and data analysis.
    Skilled in Python, SQL, TensorFlow, and Flask.
    """

    jobs = [
        {
            "title": "Machine Learning Engineer",
            "description": "Looking for Python, TensorFlow, and ML experience"
        },
        {
            "title": "Frontend Developer",
            "description": "React, JavaScript, CSS required"
        }
    ]

    skills = [
        "python", "tensorflow", "machine learning",
        "sql", "flask", "react", "javascript", "css"
    ]

    results = matcher.rank_jobs(resume, jobs, skills)

    for job in results:
        print(job)
