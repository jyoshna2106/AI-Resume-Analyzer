from flask import Flask, render_template, request
import os
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/download-report')
def download_report():

    # Create PDF
    pdf_path = "resume_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph(
        "AI Resume Analysis Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 12))

    # ATS Score
    ats = Paragraph(
        "ATS Score: 80%",
        styles['Heading2']
    )

    elements.append(ats)

    elements.append(Spacer(1, 12))

    # Skills
    skills = Paragraph(
        "Detected Skills: Python, Java, HTML",
        styles['BodyText']
    )

    elements.append(skills)

    elements.append(Spacer(1, 12))

    # Suggestions
    suggestions = Paragraph(
        "Suggestions: Learn SQL and React",
        styles['BodyText']
    )

    elements.append(suggestions)

    elements.append(Spacer(1, 12))

    # Build PDF
    doc.build(elements)

    # Download PDF
    return send_file(
        pdf_path,
        as_attachment=True
    )
# Home Page
@app.route('/')
def home():

    return render_template('index.html')


# Upload Resume
@app.route('/upload', methods=['POST'])
def upload():

    # Get uploaded file
    file = request.files['resume']

    if file:

        # Save file
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        # Read PDF
        reader = PyPDF2.PdfReader(filepath)

        # Extract text
        text = ""

        for page in reader.pages:

            text += page.extract_text()

        print("\n========== RESUME TEXT ==========\n")

        print(text)

        # Skills Database
        skills = [
            "Python",
            "Java",
            "SQL",
            "HTML",
            "CSS",
            "Machine Learning",
            "Flask",
            "React"
        ]

        # Detect Skills
        found_skills = []

        for skill in skills:

            if skill.lower() in text.lower():

                found_skills.append(skill)

        print("\n========== DETECTED SKILLS ==========\n")

        print(found_skills)

        # Missing Skills
        missing_skills = []

        for skill in skills:

            if skill not in found_skills:

                missing_skills.append(skill)

        print("\n========== MISSING SKILLS ==========\n")

        print(missing_skills)

        # ATS Score
        score = len(found_skills) * 10

        if score > 100:

            score = 100

        print("\n========== ATS SCORE ==========\n")

        print(score)

        # Interview Questions Database
        questions = {

            "Python": [
                "What is OOP in Python?",
                "Difference between list and tuple?",
                "Explain Python decorators."
            ],

            "Java": [
                "What is JVM?",
                "Explain inheritance in Java.",
                "Difference between JDK and JRE?"
            ],

            "SQL": [
                "What is JOIN?",
                "Difference between DELETE and TRUNCATE?",
                "What is normalization?"
            ],

            "HTML": [
                "What is semantic HTML?",
                "Difference between div and span?"
            ],

            "CSS": [
                "What is Flexbox?",
                "Difference between relative and absolute positioning?"
            ],

            "Flask": [
                "What is Flask?",
                "Explain Flask routing."
            ],

            "React": [
                "What is React?",
                "Explain components in React."
            ]

        }

        # Generate Questions
        generated_questions = []

        for skill in found_skills:

            if skill in questions:

                generated_questions.extend(
                    questions[skill]
                )

        print("\n========== INTERVIEW QUESTIONS ==========\n")

        print(generated_questions)

        # Resume Suggestions
        suggestions = []

        # Missing Skills Suggestions
        for skill in missing_skills:

            suggestions.append(
                f"Consider learning {skill}"
            )

        # Project Suggestion
        if "Projects" not in text:

            suggestions.append(
                "Add more project details to your resume"
            )

        # Certification Suggestion
        if "Certification" not in text and "Certifications" not in text:

            suggestions.append(
                "Add certifications to strengthen your resume"
            )

        # ATS Improvement Suggestion
        if score < 50:

            suggestions.append(
                "Improve ATS keywords in your resume"
            )

        print("\n========== SUGGESTIONS ==========\n")

        print(suggestions)

        # Job Recommendation Database
        jobs = {

            "Python": [
                "Python Developer",
                "Backend Developer"
            ],

            "Java": [
                "Java Developer",
                "Software Engineer"
            ],

            "SQL": [
                "Database Administrator",
                "Data Analyst"
            ],

            "HTML": [
                "Frontend Developer",
                "Web Designer"
            ],

            "CSS": [
                "UI Developer",
                "Frontend Developer"
            ],

            "Machine Learning": [
                "Machine Learning Engineer",
                "AI Engineer",
                "Data Scientist"
            ],

            "Flask": [
                "Backend Developer",
                "Python Web Developer"
            ],

            "React": [
                "React Developer",
                "Frontend Engineer"
            ]

        }

        # Recommended Jobs
        recommended_jobs = []

        for skill in found_skills:

            if skill in jobs:

                recommended_jobs.extend(
                    jobs[skill]
                )

        # Remove duplicates
        recommended_jobs = list(
            set(recommended_jobs)
        )

        print("\n========== RECOMMENDED JOBS ==========\n")

        print(recommended_jobs)

        # Send Data To Frontend
        return render_template(
            'result.html',
            skills=found_skills,
            missing_skills=missing_skills,
            score=score,
            questions=generated_questions,
            suggestions=suggestions,
            recommended_jobs=recommended_jobs
        )


# Run Flask App
if __name__ == '__main__':

    app.run(debug=True)