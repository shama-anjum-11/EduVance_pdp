import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# 📌 Load dataset
file_path = r'C:\Users\shama\OneDrive\Desktop\pdp bot\careerpredupdated.csv'  # Use raw string for Windows path
df = pd.read_csv(file_path)

# ✅ Check required columns
expected_columns = {'Logical_Thinking', 'Creativity', 'Analytical_Skills', 'Social_Interaction',
                    'Communication', 'Self_Motivation', 'Risk_Taking', 'Adaptability',
                    'Emotional_Intelligence', 'Technical_Skills', 'Decision_Making', 'Leadership',
                    'Curiosity', 'Career'}
if not expected_columns.issubset(df.columns):
    raise ValueError("CSV must contain all required columns.")

# 🔹 Convert 'Career' column to numerical labels
df['Career_Label'] = df['Career'].astype('category').cat.codes

# 🔹 Create mapping dictionary (stores career names for each label)
career_mapping = dict(enumerate(df['Career'].astype('category').cat.categories))

# Debug: Print the full mapping
print("✅ Career Mapping:", career_mapping)



# 🔹 Define features (X) and target (y)
X = df.drop(columns=['Career', 'Career_Label'])  # Features (all skills)
y = df['Career_Label']  # Target variable (career labels)

# 🔹 Split dataset (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, criterion='entropy', max_depth=10, random_state=42)
model.fit(X_train, y_train)

# 🔹 Define questions for user input
questions = {
    'Logical_Thinking': "1️. Do you prefer making decisions based on facts, logic, and reasoning?",
    'Creativity': "2️. Do you often think of innovative ideas?",
    'Analytical_Skills': "3️. Do you enjoy working with data and solving problems?",
    'Social_Interaction': "4️. Do you feel comfortable engaging with new people?",
    'Communication': "5️. Can you clearly express your thoughts?",
    'Self_Motivation': "6️. Do you stay committed to your tasks?",
    'Risk_Taking': "7️. Are you willing to take risks?",
    'Adaptability': "8️. Can you adjust to new situations easily?",
    'Emotional_Intelligence': "9️. Can you manage and understand emotions well?",
    'Technical_Skills': "10. Do you enjoy working with technology?",
    'Decision_Making': "11. Are you confident in making decisions under pressure?",
    'Leadership': "12. Do you take charge in group situations?",
    'Curiosity': "13. Do you explore new knowledge and ask questions?"
}

# 🔹 Function to predict career
def predict_career():
    print("\n🔎 LET'S PREDICT YOUR CAREER! 🚀")
    print("Answer the following questions on a scale of 1 to 10.\n")
    user_input = []
    
    for feature, question in questions.items():
        while True:
            try:
                value = int(input(f"{question} (1-10): "))
                if 1 <= value <= 10:
                    user_input.append(value)
                    break
                else:
                    print("⚠️ Please enter a number between 1 and 10.")
            except ValueError:
                print("⚠️ Invalid input! Please enter a valid number.")

    # Convert input into a DataFrame
    input_data = pd.DataFrame([user_input], columns=X.columns)
    
    # Predict career
    predicted_label = model.predict(input_data)[0]
    print(f"\n🎯 Recommended Career Path: {career_mapping[predicted_label]}")

predict_career()

# Save the trained model
with open("career_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save the career mapping
with open("career_mapping.pkl", "wb") as f:
    pickle.dump(career_mapping, f)

print("✅ Career model and mapping saved successfully!")






