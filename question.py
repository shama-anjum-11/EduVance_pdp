import google.generativeai as genai
import pymupdf  #for PDF processing
import os

# API key
GOOGLE_API_KEY1 = "AIzaSyBw7nQawz-0esztd2ua9f-BFEkrzZ8Qhac"  # Replace with your actual API key

# Gemini AI
genai.configure(api_key=GOOGLE_API_KEY1)

# Function to select a file locally
def select_pdf_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select a PDF File", filetypes=[("PDF Files", "*.pdf")])

    if not file_path:
        print("No file selected. Exiting.")
        exit()

    return file_path

# Function to extract text from the uploaded PDF
def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

# Function to get the user's question and process it
def process_question(document_text):
    model = genai.GenerativeModel("gemini-1.5-flash")

    print("\n Eduvance is Cooking! (Type 'thanks' to exit)\n")

    while True:
        user_question = input("You: ")
        if user_question.lower() == 'thanks':
            print("You're welcome! Have a great day! 😊")
            break

        response = model.generate_content([document_text, user_question])

        if response.text:
            print(response.text)
        else:
            print("\n Sorry, Your expected answer isn't available")

# --- Main execution flow ---

# 1. Select a PDF file
print("📄 Select your PDF file")
pdf_file = select_pdf_file()

# 2. Extract text from the PDF
document_text = extract_text_from_pdf(pdf_file)

# 3. Start the chatbot
process_question(document_text)

print("session ended")



