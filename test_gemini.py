from services.gemini_service import generate_ai_recommendation


prompt = """
Suggest 3 simple and affordable home decoration ideas
for a living room with a budget of 10000 rupees.
"""


result = generate_ai_recommendation(prompt)


print("\nGemini AI Response:\n")
print(result)