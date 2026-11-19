import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Interview",
    layout="centered"
)

# Application title
st.title("AI Interview")
st.caption("Practice and Prepare for your placement")

# Import Groq safely
try:
    from groq import Groq
except ImportError:
    st.error("Groq package is not installed.")
    st.info("Add groq to your requirements.txt file.")
    st.stop()

# API configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

# Success message
st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")

# Job role selection
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineering",
        "Data Analysis",
        "Cyber Security",
        "Software Developer",
        "Others"
    ]
)

if role == "Others":
    role = st.text_input("Enter your Job Title")

# Model selection
model = st.selectbox(
    "Choose your model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)

# Difficulty level
level = st.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
)

# Activity selection
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Activity inputs
if mode == "Generate Questions":

    count = st.slider(
        "Number of Questions", 1, 10, 5
    )

elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"]
    )

    count = st.slider(
        "Number of Questions", 1, 10, 5
    )

else:

    question = st.text_area(
        "Enter Interview Question Here"
    )

    answer = st.text_area(
        "Enter Your Answer",
        height=160
    )

# Generate AI Response
if st.button("Generate AI Response", type="primary"):

    # Input validation
    if mode in ["Evaluate Answers", "Improve Answers"]:

        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid Question and Answer.")
            st.stop()

    if mode == "Others" and not role.strip():
        st.warning("Please enter your Job Title.")
        st.stop()

    # Background information
    background = (
        f"Job Role: {role}\n"
        f"Difficulty Level: {level}\n"
    )

    # Task generation
    if mode == "Generate Questions":

        task = (
            f"Generate {count} frequently asked interview questions "
            f"for the job role {role}. "
            "Include situation-based and theory questions."
        )

    elif mode == "Generate Code Questions":

        task = (
            f"Generate {count} coding or technical questions "
            f"for {topic}. "
            "Provide hints and explain the expected approach."
        )

    elif mode == "Evaluate Answers":

        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Evaluate the answer. Identify strengths, drawbacks "
            "and areas of improvement."
        )

    elif mode == "Improve Answers":

        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Improve the answer and highlight important points."
        )

    # Combine prompt
    prompt = background + task

    # Groq API request
    try:

        with st.spinner("Generating AI Response..."):

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Act as an expert Technical Interviewer "
                            "and HR professional. "
                            "Provide accurate, clear and helpful answers."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            ai_response = response.choices[0].message.content

        # Display response
        st.subheader("AI Generated Response")
        st.markdown(ai_response)

        # Download response
        st.download_button(
            label="Download Response",
            data=ai_response,
            file_name="AI_Interview_Response.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(f"Something went wrong: {e}")
