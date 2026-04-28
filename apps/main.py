from app.agents.job_matcher import JobMatcher

if __name__ == "__main__":
    matcher = JobMatcher()

    resume = "Python developer with SQL and machine learning experience"

    jobs = [
        {"title": "ML Engineer", "description": "Python, ML, TensorFlow"},
        {"title": "Web Dev", "description": "HTML, CSS, JS"}
    ]

    skills = ["python", "sql", "machine learning", "tensorflow", "html", "css", "js"]

    results = matcher.rank_jobs(resume, jobs, skills)

    for r in results:
        print(r)
