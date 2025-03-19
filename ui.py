import streamlit as st
import google.generativeai as genai
import pymupdf  # For PDF processing

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyDnb_C37xcoo3d3NyzI8iCnK9O5TvldF4A"
genai.configure(api_key=GOOGLE_API_KEY)

def studybot_ui():
    st.header("📚 StudyBot")
    user_input = st.text_input("Ask your study-related question:")
    if st.button("Get Answer"):
        if user_input:
            model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
            response = model.generate_content(user_input)
            st.success(response.text if response.text else "Sorry, I couldn't generate a response.")
        else:
            st.warning("Please enter a question.")

def dochelp_ui():
    st.header("📄 DocHelp")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file:
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        document_text = "".join([page.get_text() for page in doc])
        
        st.text_area("Extracted Document Text:", document_text, height=200)
        user_question = st.text_input("Ask a question about the document:")
        
        if st.button("Get Answer"):
            if user_question:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([document_text, user_question])
                st.success(response.text if response.text else "Sorry, no relevant answer found.")
            else:
                st.warning("Please enter a question.")

# Main app UI
def main():
    st.set_page_config(page_title="EduVance", page_icon="🤖")
    st.title("EduVance Chatbot 🤖")
    option = st.sidebar.radio("Select a feature:", ["StudyBot", "DocHelp"])
    
    if option == "StudyBot":
        studybot_ui()
    elif option == "DocHelp":
        dochelp_ui()

if __name__ == "__main__":
    main()
