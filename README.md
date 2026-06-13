# Science Teacher Chat Tool

## Live Demo

[https://ankitsingh2820.github.io/Science-_Teacher/](https://ankitsingh2820.github.io/Science-_Teacher/)

> Note: AI responses require the Python/Flask backend to be running locally with a Gemini API key.

An interactive AI-powered chat tool that acts as an enthusiastic and patient Science Teacher. It uses the Gemini API to provide structured, step-by-step explanations for scientific concepts.

## 🚀 Features

- **Expert Teacher Persona**: Specialized "Science Professor" AI that explains complex topics to a 12-year-old level without losing accuracy.
- **Structured Responses**: Every answer includes a Direct Answer, ELI12 Explanation, Step-by-Step Example, and a Key Takeaway.
- **Science-Only Boundary**: Polished safety rules ensuring the AI stays focused on scientific subjects.
- **Modern UI**: A premium dark-mode React interface with markdown support and smooth animations.

## 🛠️ Tech Stack

- **Frontend**: React + Vite
- **Backend**: Flask (Python)
- **AI**: Google Gemini API (via `google-generativeai`)
- **Styling**: Vanilla CSS (Custom science theme)
- **Icons**: Lucide React

## 📋 Prerequisites

- Python 3.9+
- Node.js & npm
- Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

## ⚙️ Setup

1. **Clone the repository** (if applicable) and navigate to the project root.

2. **Backend Setup**:
   - Create and activate a virtual environment:
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate  # Windows
     # or
     source .venv/bin/activate  # macOS/Linux
     ```
   - Install dependencies:
     ```bash
     pip install flask flask-cors google-generativeai python-dotenv
     ```
   - Create a `.env` file in the root and add your API key:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

3. **Frontend Setup**:
   - Install npm packages:
     ```bash
     npm install
     ```

## 🏃 Running the Application

You need to run both the backend and frontend simultaneously.

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```
   *The backend will run on `http://127.0.0.1:5000`.*

2. **Start the Vite Dev Server**:
   ```bash
   npm run dev
   ```
   *The frontend will run on `http://localhost:5173`.*

3. Open [http://localhost:5173](http://localhost:5173) in your browser.

## 📁 Project Structure

```text
├── app.py              # Flask Backend API
├── .env                # API Key storage
├── package.json        # Frontend dependencies
├── vite.config.js      # Vite config with API proxy
├── src/
│   ├── main.jsx        # React entry point
│   ├── App.jsx         # Main Chat UI Logic
│   └── App.css         # Premium Styles
└── public/             # Static assets
```
