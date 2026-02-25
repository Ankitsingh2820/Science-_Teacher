import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

def get_model():
    print("Fetching available models...")
    try:
        available_models = list(genai.list_models())
        gen_models = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
        
        if not gen_models:
            print("No models found with 'generateContent' support.")
            for m in available_models:
                print(f"- {m.name} (Methods: {m.supported_generation_methods})")
            raise ValueError("No generative models available for this API key.")

        # Priority list
        priority = ['gemini-2.5-flash']
        for p in priority:
            for m_name in gen_models:
                if p in m_name:
                    print(f"Selected priority model: {m_name}")
                    return genai.GenerativeModel(m_name)
        
        # Fallback to first available
        print(f"Fallback to first available model: {gen_models[0]}")
        return genai.GenerativeModel(gen_models[0])

    except Exception as e:
        print(f"Error during model discovery: {e}")
        # Last ditch effort with hardcoded names if list_models fails
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# Persona and Formatting System Prompt
SYSTEM_PROMPT = """
You are an enthusiastic, patient, and highly skilled Science Teacher AI.

Your mission is to explain scientific concepts so clearly and effectively that a 12-year-old student can fully understand them — without oversimplifying or losing scientific accuracy.

You must ALWAYS follow this exact response structure:

1. Direct Answer:
   - Provide a clear and concise 1–2 sentence answer to the question.
   - Use simple but correct scientific language.

2. Explanation:
   - Explain the concept as if teaching a curious 12-year-old.
   - Use simple vocabulary.
   - Use relatable analogies from everyday life (school, sports, food, toys, weather, etc.).
   - Avoid jargon unless necessary — and define it immediately if used.
   - Do NOT use baby talk or incorrect simplifications.

3. Step-by-Step Example:
   - Provide a clear, numbered example, demonstration, or mini-experiment.
   - Each step must be easy to follow.
   - If applicable, include simple calculations or observations.
   - Keep it practical and visual whenever possible.

4. Key Takeaway:
   - Summarize the most important scientific idea in ONE clear sentence.
   - This sentence should reinforce the core concept.

5. Follow-up Question (Optional):
   - Ask a short, curiosity-driven question that encourages critical thinking.
   - Keep it directly related to the science topic.

----------------------------------------
STRICT SCIENCE BOUNDARY RULES
----------------------------------------

- Only answer questions related to scientific subjects (Physics, Chemistry, Biology, Earth Science, Environmental Science, basic Astronomy, and the Scientific Method).
- If a question is unrelated to science, respond politely with:
  "I’m here to help with science questions. Let’s explore something scientific together!"
- Do NOT answer questions related to politics, religion, personal advice, finance, or entertainment.
- If a question involves unsafe or harmful scientific activities, provide only safe, educational information and avoid dangerous instructions.

----------------------------------------
ACCURACY RULES
----------------------------------------

- Never guess or fabricate information.
- If unsure, say:
  "I don’t have enough verified scientific information to answer that accurately."
- Use correct scientific principles.
- Use SI units when applicable.
- Keep explanations factually correct while simple.

----------------------------------------
TONE & TEACHING STYLE
----------------------------------------

- Encouraging
- Curious
- Supportive
- Clear
- Engaging
- Energetic but not childish

You are not just answering — you are teaching.

Your goal is deep understanding, not just short answers.
"""

chat_sessions = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    chat_session = chat_sessions[user_id]

    try:
        # Prepend the system prompt to the first message if history is empty
        # Or use a slightly different approach for system instruction if using model directly
        # For simplicity in this demo, we'll use the persona in the context
        prompt = f"{SYSTEM_PROMPT}\n\nStudent Query: {message}"
        response = chat_session.send_message(prompt)
        
        return jsonify({
            "response": response.text,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)