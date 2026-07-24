import streamlit as st
from utils.resume_parser import extract_text_from_uploaded_file
from utils.analyzer import analyze_resume, generate_text_report

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and paste a job description to receive an ATS score, "
    "skill analysis, missing skills, and improvement suggestions."
)

with st.sidebar:
    st.header("About")
    st.info(
        "This educational project uses Natural Language Processing, "
        "TF-IDF, cosine similarity, and skill matching."
    )
    st.warning(
        "The score is an educational estimate and not an official company ATS score."
    )

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Paste the job description here..."
)

analyze_button = st.button(
    "Analyze Resume",
    use_container_width=True,
    type="primary"
)

if analyze_button:
    if uploaded_file is None:
        st.error("Please upload a resume.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_text_from_uploaded_file(uploaded_file)
                result = analyze_resume(resume_text, job_description)

            if not resume_text.strip():
                st.error("No readable text was found in the uploaded resume.")
                st.stop()

            st.success("Resume analysis completed.")

            col1, col2, col3 = st.columns(3)
            col1.metric("ATS Match Score", f"{result['ats_score']}%")
            col2.metric("Resume Skills Found", len(result["resume_skills"]))
            col3.metric("Missing Job Skills", len(result["missing_skills"]))

            st.progress(result["ats_score"] / 100)

            left, right = st.columns(2)

            with left:
                st.subheader("✅ Skills Found in Resume")
                if result["resume_skills"]:
                    st.write(", ".join(result["resume_skills"]))
                else:
                    st.info("No known technical skills were identified.")

                st.subheader("🎯 Matching Skills")
                if result["matching_skills"]:
                    st.write(", ".join(result["matching_skills"]))
                else:
                    st.info("No matching skills were detected.")

                st.subheader("💼 Suggested Job Roles")
                if result["recommended_roles"]:
                    for role in result["recommended_roles"]:
                        st.write(f"- {role}")
                else:
                    st.info("Add more technical skills to receive job-role suggestions.")

            with right:
                st.subheader("⚠️ Missing Skills")
                if result["missing_skills"]:
                    st.write(", ".join(result["missing_skills"]))
                else:
                    st.success("No important skills are missing from the current skill list.")

                st.subheader("📌 Resume Suggestions")
                for suggestion in result["suggestions"]:
                    st.write(f"- {suggestion}")

                st.subheader("📊 Score Details")
                st.write(f"Text similarity score: {result['similarity_score']}%")
                st.write(f"Skill match score: {result['skill_match_score']}%")
                st.write(f"Resume word count: {result['word_count']}")

            report = generate_text_report(result)

            st.download_button(
                label="Download Analysis Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

            with st.expander("View Extracted Resume Text"):
                st.text_area(
                    "Extracted Text",
                    resume_text,
                    height=300,
                    disabled=True
                )

        except Exception as error:
            st.error(f"Unable to analyze the resume: {error}")
