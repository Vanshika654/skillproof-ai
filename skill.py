
import streamlit as st
from database import (
    initialize_database,
    save_profile,
    load_latest_profile,
    save_assessment,
    load_latest_assessment,
    save_project,
    load_projects
)
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
initialize_database()
ROLE_SKILLS = {
    "Python Developer": [
        "Python", "SQL", "Git", "Data Structures",
        "Problem Solving"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "Git",
        "Responsive Design"
    ],
    "AI/ML Engineer": [
        "Python", "Statistics", "Machine Learning",
        "NumPy", "Pandas"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Statistics",
        "Data Visualization"
    ]
}


def create_skill_report_pdf(profile, score, total, projects):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    styles["Title"].textColor = colors.HexColor("#0B1630")
    styles["Heading2"].textColor = colors.HexColor("#0F766E")

    content = []

    content.append(Paragraph("SkillProof AI", styles["Title"]))
    content.append(
        Paragraph("Student Skill Report", styles["Heading2"])
    )
    content.append(Spacer(1, 16))

    content.append(Paragraph("Student Overview", styles["Heading2"]))

    content.append(Paragraph(
        f"Name: {profile.get('name', 'Not provided')}",
        styles["BodyText"]
    ))
    content.append(Paragraph(
        f"College: {profile.get('college', 'Not provided')}",
        styles["BodyText"]
    ))
    content.append(Paragraph(
        f"Target Role: {profile.get('target_role', 'Not provided')}",
        styles["BodyText"]
    ))

    skills = profile.get("skills", [])
    content.append(Paragraph(
        "Skills: " + (", ".join(skills) if skills else "Not added"),
        styles["BodyText"]
    ))
    content.append(Spacer(1, 16))

    content.append(Paragraph("Assessment Results", styles["Heading2"]))

    if score is not None and total:
        percentage = round(score / total * 100)
        content.append(Paragraph(
            f"Demo Quiz Score: {score}/{total} ({percentage}%)",
            styles["BodyText"]
        ))
    else:
        content.append(Paragraph(
            "No assessment completed yet.",
            styles["BodyText"]
        ))

    content.append(Spacer(1, 16))
    content.append(Paragraph("Projects", styles["Heading2"]))

    if projects:
        for project in projects:
            content.append(Paragraph(
                project.get("name", "Untitled Project"),
                styles["Heading3"]
            ))
            content.append(Paragraph(
                project.get("description", "No description provided."),
                styles["BodyText"]
            ))
            content.append(Paragraph(
                "Category: " + project.get("category", "Not specified"),
                styles["BodyText"]
            ))
            content.append(Spacer(1, 8))
    else:
        content.append(Paragraph(
            "No projects added yet.",
            styles["BodyText"]
        ))

    content.append(Spacer(1, 20))
    content.append(Paragraph(
        "Disclaimer: Assessment results are from a demo quiz "
        "and are not verified credentials.",
        styles["Italic"]
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()

st.set_page_config(
    page_title="SkillProof AI",
    page_icon="🎯",
    layout="wide"
)

# Design


st.markdown("""
<style>
/* Main app background and text */
.stApp {
    background-color: #F3F6FB;
    color: #17233B;
}

[data-testid="stAppViewContainer"] {
    background-color: #F3F6FB;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* Main headings and normal text */
h1, h2, h3, h4, p, label,
[data-testid="stMarkdownContainer"] {
    color: #17233B;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0B1630;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Text inputs and text areas */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #17233B !important;
    -webkit-text-fill-color: #17233B !important;
    border: 1px solid #B8C5D8 !important;
    border-radius: 8px !important;
}

/* Dropdowns and selected values */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #17233B !important;
    border-color: #B8C5D8 !important;
}

[data-baseweb="select"] input {
    color: #17233B !important;
    -webkit-text-fill-color: #17233B !important;
}

/* Dropdown menu options */
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #FFFFFF !important;
}

[role="option"] {
    background-color: #FFFFFF !important;
    color: #17233B !important;
}

/* Radio buttons, checkboxes and form labels */
.stRadio label,
.stCheckbox label,
.stMultiSelect label,
.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stNumberInput label {
    color: #17233B !important;
}

/* Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 12px;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #0F766E;
    color: #FFFFFF !important;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #115E59;
    color: #FFFFFF !important;
}

/* Links */
a {
    color: #087F8C !important;
}

/* Hero banner */
.hero {
    background: linear-gradient(120deg, #0B1630, #15515A);
    padding: 35px;
    border-radius: 18px;
    color: #FFFFFF;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 42px;
}

.hero p {
    color: #D5E7EF !important;
    font-size: 18px;
}

/* Alerts and metric values */
[data-testid="stAlert"] p {
    color: inherit;
}

[data-testid="stMetricValue"] {
    color: #17233B;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.title("🎯 SkillProof AI")
st.sidebar.caption("Prove your skills. Unlock opportunities.")

pages = [
    "Dashboard",
    "My Profile",
    "Skill Assessment",
    "Projects",
    "Skill Report",
    "Skill Gap Analysis",
    "Learning Roadmap",
    "My Portfolio"
]

if "dashboard_destination" in st.session_state:
    default_page = st.session_state.pop("dashboard_destination")
    default_index = pages.index(default_page)
else:
    default_index = 0

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=default_index,
    key="main_navigation"
)

# Dashboard

if page == "Dashboard":
    profile = st.session_state.get("student_profile", {})
    score = st.session_state.get("assessment_score")
    total = st.session_state.get("assessment_total", 0)
    projects = st.session_state.get("projects", [])

    st.markdown("""
    <div class="hero">
        <h1>SkillProof AI</h1>
        <p>Don't just list your skills. Prove what you can do.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    student_name = profile.get("name", "").strip()

    if student_name:
        st.subheader(f"Welcome back, {student_name}! 👋")
    else:
        st.subheader("Welcome to your skill journey! 👋")

    st.write(
        "Build your profile, test your knowledge, and showcase "
        "your projects — all in one place."
    )

    st.divider()
    st.subheader("📈 Your Progress")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Skills Added",
            len(profile.get("skills", []))
        )

    with col2:
        if score is not None and total:
            st.metric("Latest Quiz Score", f"{score}/{total}")
        else:
            st.metric("Latest Quiz Score", "Not attempted")

    with col3:
        st.metric("Projects Added", len(projects))

    st.divider()
    st.subheader("🚀 Continue Building Your Proof")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Complete Your Profile")
        st.write("Add your skills, target role, and career introduction.")
        if st.button("Open My Profile", use_container_width=True):
            st.session_state["dashboard_destination"] = "My Profile"
            st.rerun()

        st.markdown("### 🧠 Test Your Knowledge")
        st.write("Attempt the Python fundamentals assessment.")
        if st.button("Start Assessment", use_container_width=True):
            st.session_state["dashboard_destination"] = "Skill Assessment"
            st.rerun()

    with col2:
        st.markdown("### 📁 Showcase Your Projects")
        st.write("Add project descriptions and links to your work.")
        if st.button("Open Projects", use_container_width=True):
            st.session_state["dashboard_destination"] = "Projects"
            st.rerun()

        st.markdown("### 📊 View Your Skill Report")
        st.write("Review your profile, quiz results, and project portfolio.")
        if st.button("View Skill Report", use_container_width=True):
            st.session_state["dashboard_destination"] = "Skill Report"
            st.rerun()

    st.divider()
    st.caption(
        "Prototype notice: progress reflects information entered in "
        "your current app session."
    )



elif page == "My Profile":
    st.title("👤 My Profile")
    st.write("Build your professional student profile.")

    saved_profile = load_latest_profile()

    with st.form("student_profile_form"):
        name = st.text_input(
            "Full Name",
            value=saved_profile.get("name", "")
        )

        college = st.text_input(
            "College",
            value=saved_profile.get("college", "")
        )

        year = st.selectbox(
            "Current Year",
            ["1st Year", "2nd Year", "3rd Year", "4th Year"],
            index=(
                ["1st Year", "2nd Year", "3rd Year", "4th Year"].index(
                    saved_profile["year"]
                )
                if saved_profile.get("year") in [
                    "1st Year", "2nd Year", "3rd Year", "4th Year"
                ]
                else 0
            )
        )

        target_role = st.selectbox(
            "Target Career Role",
            [
                "Python Developer",
                "Web Developer",
                "AI/ML Engineer",
                "Data Analyst",
                "Software Engineer"
            ],
            index=(
                [
                    "Python Developer",
                    "Web Developer",
                    "AI/ML Engineer",
                    "Data Analyst",
                    "Software Engineer"
                ].index(saved_profile["target_role"])
                if saved_profile.get("target_role") in [
                    "Python Developer",
                    "Web Developer",
                    "AI/ML Engineer",
                    "Data Analyst",
                    "Software Engineer"
                ]
                else 0
            )
        )

        skills = st.multiselect(
            "Your Skills",
            [
                "Python",
                "C++",
                "HTML",
                "CSS",
                "JavaScript",
                "SQL",
                "Git",
                "Data Structures",
                "Problem Solving",
                "Statistics",
                "Machine Learning",
                "NumPy",
                "Pandas",
                "Excel",
                "Data Visualization",
                "Responsive Design"
            ],
            default=saved_profile.get("skills", [])
        )

        about = st.text_area(
            "About You",
            value=saved_profile.get("about", ""),
            placeholder="Write a short introduction about yourself."
        )

        submitted = st.form_submit_button("💾 Save Profile")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            save_profile(
                name.strip(),
                college.strip(),
                year,
                target_role,
                skills,
                about.strip()
            )

            st.session_state["student_profile"] = {
                "name": name.strip(),
                "college": college.strip(),
                "year": year,
                "target_role": target_role,
                "skills": skills,
                "about": about.strip()
            }

            st.success("Your profile has been saved permanently!")

    st.divider()
    st.subheader("👀 Profile Preview")

    current_profile = st.session_state.get(
        "student_profile",
        saved_profile
    )

    if current_profile:
        st.write("**Name:**", current_profile.get("name", ""))
        st.write("**College:**", current_profile.get("college", ""))
        st.write("**Year:**", current_profile.get("year", ""))
        st.write(
            "**Target Role:**",
            current_profile.get("target_role", "")
        )

        current_skills = current_profile.get("skills", [])
        st.write(
            "**Skills:**",
            ", ".join(current_skills) if current_skills else "None added"
        )
        st.write("**About:**", current_profile.get("about", ""))
    else:
        st.info("Enter your details above and save your profile.")

elif page == "Skill Assessment":
    st.title("🧠 Skill Assessment")
    st.write("Test your Python fundamentals.")

    questions = [
        {
            "question": "1. Which data type stores key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary"
        },
        {
            "question": "2. What is the output of len([10, 20, 30])?",
            "options": ["2", "3", "10", "30"],
            "answer": "3"
        },
        {
            "question": "3. Which keyword defines a function in Python?",
            "options": ["function", "def", "fun", "define"],
            "answer": "def"
        },
        {
            "question": "4. Which symbol starts a comment in Python?",
            "options": ["//", "<!--", "#", "/*"],
            "answer": "#"
        },
        {
            "question": "5. What does 2 ** 3 return?",
            "options": ["5", "6", "8", "9"],
            "answer": "8"
        }
    ]

    with st.form("python_assessment"):
        answers = []

        for i, q in enumerate(questions):
            st.markdown(f"**{q['question']}**")

            choice = st.radio(
                "Choose your answer:",
                q["options"],
                index=None,
                key=f"python_q_{i}"
            )

            answers.append(choice)

        submitted = st.form_submit_button("Submit Assessment")

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer all questions before submitting.")
        else:
            score = sum(
                answer == q["answer"]
                for answer, q in zip(answers, questions)
            )

            percentage = (score / len(questions)) * 100

            st.session_state["assessment_score"] = score
            st.session_state["assessment_total"] = len(questions)
            st.session_state["assessment_percentage"] = percentage

            st.divider()
            st.subheader("Your Assessment Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Score", f"{score}/{len(questions)}")

            with col2:
                st.metric("Accuracy", f"{percentage:.0f}%")

            st.progress(percentage / 100)

            if percentage >= 80:
                st.success("Excellent! You have a strong foundation.")
            elif percentage >= 60:
                st.info("Good effort! Revise a few concepts and practise more.")
            else:
                st.warning("Keep learning! Review the fundamentals and try again.")

            st.caption(
                "Demo assessment only. This score measures performance "
                "on these five questions, not overall job readiness."
            )



elif page == "Projects":
    st.title("🚀 My Projects")
    st.write("Add your projects to build your skill portfolio.")

    with st.form("project_form"):
        project_name = st.text_input("Project Name")

        category = st.selectbox(
            "Project Category",
            ["AI/ML", "Web Development", "Data Science", "Other"]
        )

        description = st.text_area("Project Description")
        technologies = st.text_input(
            "Technologies Used",
            placeholder="Python, Streamlit, SQLite"
        )
        github = st.text_input("GitHub Repository URL")
        demo = st.text_input("Live Demo URL")

        submitted = st.form_submit_button("💾 Save Project")

    if submitted:
        if not project_name.strip():
            st.error("Please enter a project name.")
        else:
            save_project(
                project_name.strip(),
                category,
                description.strip(),
                technologies.strip(),
                github.strip(),
                demo.strip()
            )

            st.success("Project saved permanently!")

    st.divider()
    st.subheader("📁 Your Saved Projects")

    saved_projects = load_projects()

    if saved_projects:
        for project in saved_projects:
            with st.container(border=True):
                st.subheader(project["name"])
                st.write("**Category:**", project["category"])
                st.write(
                    "**Description:**",
                    project["description"] or "Not provided"
                )
                st.write(
                    "**Technologies:**",
                    project["technologies"] or "Not provided"
                )

                if project["github"]:
                    st.markdown(
                        f"[View GitHub Repository]({project['github']})"
                    )

                if project["demo"]:
                    st.markdown(
                        f"[Open Live Demo]({project['demo']})"
                    )
    else:
        st.info("No projects saved yet. Add your first project above.")



elif page == "Skill Report":
    st.title("📊 My Skill Report")
    st.write(
        "Your skills, assessment results, and projects in one place."
    )

    profile = st.session_state.get("student_profile", {})
    score = st.session_state.get("assessment_score")
    total = st.session_state.get("assessment_total", 0)
    projects = st.session_state.get("projects", [])

    st.divider()

    # Student overview
    st.subheader("👤 Student Overview")

    if profile:
        st.write("**Name:**", profile.get("name", "Not provided"))
        st.write("**College:**", profile.get("college", "Not provided"))
        st.write("**Target Role:**", profile.get("target_role", "Not provided"))

        skills = profile.get("skills", [])
        st.write(
            "**Skills:**",
            ", ".join(skills) if skills else "No skills added yet"
        )
    else:
        st.info("Complete My Profile first.")

    st.divider()

    # Assessment performance
    st.subheader("🧠 Assessment Performance")

    if score is not None and total:
        percentage = round((score / total) * 100)

        col1, col2 = st.columns(2)
        col1.metric("Quiz Score", f"{score}/{total}")
        col2.metric("Percentage", f"{percentage}%")

        st.progress(percentage / 100)
        st.caption("Demo quiz result, not a verified certification.")
    else:
        st.info("Complete the Skill Assessment to see your score.")

    st.divider()

    # Project portfolio
    st.subheader("📁 Project Portfolio")
    st.metric("Projects Added", len(projects))

    if projects:
        for project in projects:
            st.markdown(f"### {project.get('name', 'Untitled Project')}")
            st.write(project.get("description", "No description added."))
            st.caption(
                f"Category: {project.get('category', 'Not specified')}"
            )
    else:
        st.info("Add a project in the Projects section.")

    # Downloadable report
    st.divider()
    st.subheader("📥 Download Your Report")

    report_lines = [
        "SKILLPROOF AI - STUDENT SKILL REPORT",
        "=" * 40,
        "",
        f"Name: {profile.get('name', 'Not provided')}",
        f"College: {profile.get('college', 'Not provided')}",
        f"Target Role: {profile.get('target_role', 'Not provided')}",
        "",
        "SKILLS",
        ", ".join(profile.get("skills", [])) or "No skills added",
        "",
        "ASSESSMENT",
    ]

    if score is not None and total:
        report_lines.append(f"Score: {score}/{total}")
        report_lines.append(f"Percentage: {round(score / total * 100)}%")
    else:
        report_lines.append("No assessment completed yet")

    report_lines.extend(["", "PROJECTS"])

    if projects:
        for project in projects:
            report_lines.extend([
                f"Name: {project.get('name', 'Untitled')}",
                f"Category: {project.get('category', 'Not specified')}",
                f"Description: {project.get('description', '')}",
                f"Technologies: {project.get('technologies', '')}",
                f"GitHub: {project.get('github', '')}",
                f"Live Demo: {project.get('demo', '')}",
                ""
            ])
    else:
        report_lines.append("No projects added yet.")

    report_lines.extend([
        "",
        "Note: Assessment results are from a demo quiz.",
        "This report is not a verified credential."
    ])

    
    
    st.divider()
    st.subheader("📥 Download PDF Skill Report")

    pdf_data = create_skill_report_pdf(
        profile, score, total, projects
    )

    st.download_button(
        label="📄 Download PDF Skill Report",
        data=pdf_data,
        file_name="SkillProof_AI_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

elif page == "Skill Gap Analysis":
    st.title("🎯 Skill Gap Analysis")
    st.write(
        "Identify skills to improve for your target career role."
    )

    profile = st.session_state.get("student_profile", {})
    student_skills = profile.get("skills", [])

    role = st.selectbox(
        "Choose your target role",
        list(ROLE_SKILLS.keys())
    )

    required_skills = ROLE_SKILLS[role]

    # Match skills without case sensitivity
    normalized_skills = {
        skill.strip().lower() for skill in student_skills
    }

    matched_skills = [
        skill for skill in required_skills
        if skill.lower() in normalized_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in normalized_skills
    ]

    match_percentage = round(
        len(matched_skills) / len(required_skills) * 100
    )

    st.divider()
    st.subheader(f"📊 Your Match for {role}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Skills Matched", len(matched_skills))
    col2.metric("Skills to Develop", len(missing_skills))
    col3.metric("Skill Match", f"{match_percentage}%")

    st.progress(match_percentage / 100)

    st.caption(
        "This percentage measures listed-skill overlap only. "
        "It does not measure actual proficiency or job readiness."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills You Listed")

        if matched_skills:
            for skill in matched_skills:
                st.success(skill)
        else:
            st.info("No matching skills listed yet.")

    with col2:
        st.subheader("📚 Skills to Develop")

        if missing_skills:
            for skill in missing_skills:
                st.warning(skill)
        else:
            st.success("All listed role skills are matched!")

    st.divider()
    st.subheader("🚀 Suggested Next Step")

    if missing_skills:
        next_skill = missing_skills[0]
        st.write(
            f"Start by learning **{next_skill}**. "
            "Study the basics, practise exercises, and build "
            "a small project to demonstrate your understanding."
        )
    else:
        st.write(
            "Review your knowledge and build projects that "
            "demonstrate your listed skills."
        )

    if not profile:
        st.info(
            "Tip: Complete My Profile and add your skills "
            "to get a more useful comparison."
        )

elif page == "Learning Roadmap":
    st.title("🗺️ Personalized Learning Roadmap")
    st.write(
        "Turn your skill gaps into small, achievable learning goals."
    )

    profile = st.session_state.get("student_profile", {})
    student_skills = profile.get("skills", [])

    role = st.selectbox(
        "Choose your target role",
        list(ROLE_SKILLS.keys()),
        key="roadmap_role"
    )

    required_skills = ROLE_SKILLS[role]

    normalized_skills = {
        skill.strip().lower() for skill in student_skills
    }

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in normalized_skills
    ]

    st.divider()

    if not missing_skills:
        st.success(
            "No skill gaps found in this basic comparison. "
            "You can still strengthen your skills with projects."
        )
    else:
        st.subheader("📅 Your 4-Week Starter Plan")

        roadmap = {
            1: missing_skills[0:1],
            2: missing_skills[1:2],
            3: missing_skills[2:4],
            4: missing_skills[4:]
        }

        learning_tasks = {
            "Python": "Learn syntax, functions, and practise coding problems.",
            "SQL": "Practise SELECT, WHERE, JOIN, and GROUP BY queries.",
            "Git": "Learn repositories, commits, branches, and GitHub.",
            "Data Structures": "Practise arrays, strings, stacks, and queues.",
            "Problem Solving": "Solve beginner problems and explain your approach.",
            "HTML": "Build a structured multi-page webpage.",
            "CSS": "Practise layouts, Flexbox, and responsive styling.",
            "JavaScript": "Learn variables, functions, arrays, and DOM basics.",
            "Responsive Design": "Make a webpage usable on mobile and desktop.",
            "Statistics": "Study averages, probability, distributions, and variance.",
            "Machine Learning": "Understand train/test splits and basic models.",
            "NumPy": "Practise arrays and numerical operations.",
            "Pandas": "Load, clean, filter, and analyse tabular data.",
            "Excel": "Practise formulas, sorting, filtering, and pivot tables.",
            "Data Visualization": "Create clear charts from a small dataset."
        }

        for week, skills in roadmap.items():
            with st.expander(f"Week {week}", expanded=(week == 1)):
                if skills:
                    for skill in skills:
                        st.markdown(f"**{skill}**")
                        st.write(
                            learning_tasks.get(
                                skill,
                                f"Study the fundamentals of {skill} "
                                "and practise with small exercises."
                            )
                        )

                        st.checkbox(
                            f"Mark {skill} as completed",
                            key=f"roadmap_{role}_{week}_{skill}"
                        )
                else:
                    st.write(
                        "Review previous topics, revise your notes, "
                        "and build a small project using what you learned."
                    )

        st.divider()
        st.info(
            "This is a starter roadmap based on predefined skill gaps. "
            "Adjust the pace according to your schedule and current level."
        )

elif page == "My Portfolio":
    st.title("🌐 My SkillProof Portfolio")
    st.write(
        "A professional overview of your skills, learning, and projects."
    )

    profile = st.session_state.get("student_profile", {})
    score = st.session_state.get("assessment_score")
    total = st.session_state.get("assessment_total", 0)
    projects = st.session_state.get("projects", [])

    student_name = profile.get("name", "").strip()
    target_role = profile.get("target_role", "Aspiring Professional")
    skills = profile.get("skills", [])

    st.divider()

    # Portfolio header
    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #0B1630, #15515A);
            padding: 30px;
            border-radius: 18px;
            color: white;
        ">
            <h1 style="color:white; margin-bottom:8px;">
                SkillProof AI
            </h1>
            <p style="color:#D5E7EF; font-size:18px;">
                Skills backed by learning and project evidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if student_name:
        st.header(student_name)
    else:
        st.header("Your Name")
        st.info("Add your name in My Profile to personalize your portfolio.")

    st.write(f"**Career Goal:** {target_role}")

    if profile.get("college"):
        st.write(f"**College:** {profile['college']}")

    st.divider()

    # Skills
    st.subheader("💡 Skills")

    if skills:
        st.write("  •  ".join(skills))
    else:
        st.info("Add your skills in My Profile.")

    st.divider()

    # Assessment
    st.subheader("🧠 Assessment Evidence")

    if score is not None and total:
        percentage = round(score / total * 100)

        col1, col2 = st.columns(2)
        col1.metric("Demo Quiz Score", f"{score}/{total}")
        col2.metric("Percentage", f"{percentage}%")

        st.caption(
            "This is a demo quiz result, not a verified certification."
        )
    else:
        st.info("Complete a Skill Assessment to display your result.")

    st.divider()

    # Projects
    st.subheader("📁 Featured Projects")

    if projects:
        for project in projects:
            with st.container(border=True):
                st.markdown(
                    f"### {project.get('name', 'Untitled Project')}"
                )
                st.write(
                    project.get("description", "No description provided.")
                )
                st.caption(
                    f"Category: {project.get('category', 'Not specified')}"
                )

                technologies = project.get("technologies", "")
                if technologies:
                    st.write(f"**Technologies:** {technologies}")

                github = project.get("github", "")
                demo = project.get("demo", "")

                if github:
                    st.markdown(f"[View GitHub Project]({github})")
                if demo:
                    st.markdown(f"[Open Live Demo]({demo})")
    else:
        st.info("Add a project in the Projects section to showcase your work.")

    st.divider()

    st.caption(
        "Portfolio preview generated by SkillProof AI. "
        "Information is user-provided and has not been independently verified."
    )

    # Download a simple portfolio summary
    portfolio_text = [
        "SKILLPROOF AI — STUDENT PORTFOLIO",
        "=" * 38,
        "",
        f"Name: {student_name or 'Not provided'}",
        f"College: {profile.get('college', 'Not provided')}",
        f"Career Goal: {target_role}",
        f"Skills: {', '.join(skills) if skills else 'Not provided'}",
        "",
        "ASSESSMENT",
        f"Score: {score}/{total}" if score is not None and total else
        "No assessment completed yet",
        "",
        "PROJECTS"
    ]

    for project in projects:
        portfolio_text.extend([
            f"Project: {project.get('name', 'Untitled Project')}",
            f"Description: {project.get('description', '')}",
            f"Technologies: {project.get('technologies', '')}",
            f"GitHub: {project.get('github', '')}",
            f"Live Demo: {project.get('demo', '')}",
            ""
        ])

    st.download_button(
        "⬇️ Download Portfolio Summary",
        data="\n".join(portfolio_text),
        file_name="SkillProof_AI_Portfolio.txt",
        mime="text/plain",
        use_container_width=True
    )
