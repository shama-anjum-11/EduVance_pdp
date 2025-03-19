import streamlit as st
import google.generativeai as genai
import pymupdf  # For PDF processing
import pandas as pd
import pickle

# Configure Gemini AI
genai.configure(api_key="AIzaSyDnb_C37xcoo3d3NyzI8iCnK9O5TvldF4A")

# Load Pretrained Models
studybot_model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
dochelp_model = genai.GenerativeModel("gemini-1.5-flash")

# Load Career Prediction Model
with open("career_model.pkl", "rb") as f:
    career_model = pickle.load(f)

# Load Career Mapping Dictionary
with open("career_mapping.pkl", "rb") as f:
    career_mapping = pickle.load(f)

# Career Mapping Dictionary (Ensure this matches the categories in your dataset)
career_mapping = {
    0: "AI Engineer",
    1: "Actor",
    2: "Architect",
    3: "Artist",
    4: "Baker",
    5: "Business Analyst" ,
    6: "Data Scientist" ,
    7: "Designer",
    8: "Doctor",
    9: "Economist",
    10: "Engineer",
    11: "Entrepreneur",
    12: "Food Vlogger",
    13: "Influencer",
    14: "Lawyer",
    15: "Marketing Specialist",
    16: "Musician",
    17: "Poet",
    18: "Professor",
    19: "Psychologist",
    20: "Researcher",
    21: "Scientist",
    22: "Software Developer",
    23: "Teacher",
    24: "Writer",
    25: "YouTuber",
}  # Update this mapping based on your dataset

# Define career-related questions
questions = {
    'Logical_Thinking': "Do you prefer making decisions based on logic and reasoning?",
    'Creativity': "Do you often think of innovative ideas?",
    'Analytical_Skills': "Do you enjoy working with data and solving problems?",
    'Social_Interaction': "Do you feel comfortable engaging with new people?",
    'Communication': "Can you clearly express your thoughts?",
    'Self_Motivation': "Do you stay committed to your tasks?",
    'Risk_Taking': "Are you willing to take risks?",
    'Adaptability': "Can you adjust to new situations easily?",
    'Emotional_Intelligence': "Can you manage and understand emotions well?",
    'Technical_Skills': "Do you enjoy working with technology?",
    'Decision_Making': "Are you confident in making decisions under pressure?",
    'Leadership': "Do you take charge in group situations?",
    'Curiosity': "Do you explore new knowledge and ask questions?"
}

# App Title
st.set_page_config(page_title="EduVance", page_icon="🤖")
st.title("🤖 EduVance")

from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu(
        menu_title = "Menu",
        options = ["StudyBot", "DocHelp", "Career Suggestion"],
        icons= ["robot","file-earmark","journals"],
        menu_icon= "list",
        default_index=0,
        )


# StudyBot Feature
if selected == "StudyBot":
    st.subheader("📚 StudyBot - Ask Anything!")

    # Chat History
    if "studybot_history" not in st.session_state:
        st.session_state.studybot_history = []

    # Display Chat History
    for msg in st.session_state.studybot_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Ask me anything about your studies...")
    
    if user_input:
        st.session_state.studybot_history.append({"role": "user", "content": user_input})
        response = studybot_model.generate_content(user_input).text
        st.session_state.studybot_history.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

# DocHelp Feature
elif selected == "DocHelp":
    st.subheader("📄 DocHelp - Upload a File & Ask Questions!")

    # File Uploader
    uploaded_file = st.file_uploader("Upload a document", type="pdf")

    if uploaded_file:
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        document_text = "".join([page.get_text() for page in doc])

        # Chat History
        if "dochelp_history" not in st.session_state:
            st.session_state.dochelp_history = []

        # Display Chat History
        for msg in st.session_state.dochelp_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User Input
        user_question = st.chat_input("Ask a question about the document...")
        
        if user_question:
            st.session_state.dochelp_history.append({"role": "user", "content": user_question})
            response = dochelp_model.generate_content([document_text, user_question]).text
            st.session_state.dochelp_history.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)

# Career Prediction Feature
if selected == "Career Suggestion":
    st.subheader("🎯 Find Your Best Fit!")

    # Collect user inputs
    user_responses = {feature: st.slider(question, 1, 10, 5) for feature, question in questions.items()}


    if st.button("Results"):
        try:
            input_data = pd.DataFrame([list(user_responses.values())], columns=user_responses.keys())

            # Predict Career
            predicted_label = career_model.predict(input_data)[0]


            # Ensure the label exists in the mapping
            if predicted_label in career_mapping:
                predicted_career = career_mapping[predicted_label]
            else:
                predicted_career = "⚠️ Sorry, We are facing some issues"

            # Show final prediction
            st.success(f"🎯 Recommended Career Path: {predicted_career}")

        except Exception as e:
            st.error(f"⚠️ Error in Career Prediction: {e}")






