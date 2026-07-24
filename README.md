# AI Resume Analyzer

A beginner-friendly Natural Language Processing project that analyzes a resume against a job description.

## Main Features

- Upload PDF, DOCX, or TXT resumes
- Extract resume text
- Calculate an educational ATS match score
- Identify resume skills
- Identify matching and missing job skills
- Recommend suitable job roles
- Provide resume improvement suggestions
- Download an analysis report
- Simple Streamlit web interface

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- PyPDF2
- python-docx
- JSON

## Project Structure

```text
AI_Resume_Analyzer/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── skills.json
│   └── job_roles.json
├── utils/
│   ├── __init__.py
│   ├── analyzer.py
│   └── resume_parser.py
└── screenshots/
    └── add-screenshot-here.txt
```

## How It Works

1. The user uploads a resume.
2. Text is extracted from PDF, DOCX, or TXT.
3. Resume text is compared with the job description.
4. TF-IDF converts text into numerical vectors.
5. Cosine similarity measures text similarity.
6. Skill matching compares resume skills with job-description skills.
7. The final ATS score combines text similarity and skill matching.
8. The app displays missing skills and improvement suggestions.

## Installation

Open the project folder in PyCharm.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
streamlit run app.py
```

The application normally opens at:

```text
http://localhost:8501
```

## ATS Score Formula

```text
ATS Score =
55% Text Similarity +
45% Skill Match
```

This score is only an educational estimate. Real ATS platforms may use different rules.

## Sample Job Description

```text
We are looking for a Java Developer with knowledge of Java, Spring Boot,
SQL, REST API, Git, teamwork, and problem-solving skills.
```

## Future Enhancements

- Grammar checking
- Resume section detection
- AI-generated resume summary
- PDF report generation
- User login and analysis history
- Multiple resume comparison
- Cloud deployment

## Author

Saranya K  
B.Tech Computer Science and Engineering

## Disclaimer

This project is intended for educational use. It does not reproduce the exact scoring method of any company's applicant-tracking system.
