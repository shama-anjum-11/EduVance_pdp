import google.generativeai as genai

# Directly pass your API key here
GOOGLE_API_KEY = "AIzaSyDnb_C37xcoo3d3NyzI8iCnK9O5TvldF4A"  #API key

# Configure the Gemini AI client
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

print("Hello! Welcome to Eduvance, how can we help you? (Type 'thanks' to exit)")

while True:
    user_input = input("\nYou: ")  #user input
    
    if user_input.lower() == "thanks":  # Exit condition
        print(" You're welcome! Have a great day! 😊")
        break
    
    # Generate response
    response = model.generate_content(user_input)
    
    # Print response
    if response.text:
        print(response.text)
    else:
        print("\n Sorry, I couldn't generate a response.")

