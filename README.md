# 🧠 AI Exam Assistant

An intelligent, on-screen assistant that helps you during open-book exams by extracting text from a screenshot and providing AI-generated answers in a pop-up window.

---

## 🚀 Features

- 📸 Custom screenshot capture tool.
- 🧾 OCR to extract question text.
- 💡 Local AI (LLaMA3 via Ollama) generates full answers (code, MCQ, theory).
- 🪟 Answers shown in a floating window.
- 🔊 Text-to-Speech (TTS) to read out answers.
- 📋 Copy answer to clipboard.
- 📄 Save answer to `.txt` or `.pdf`.
- 🎛️ Toggle answer display and scroll freely.
- 🧵 Multi-threaded for smooth experience.

---

## 🖥️ How it Works

1. Press `Ctrl + Alt + V` to open the assistant.
2. Click **"Capture Screenshot"** and drag over the question on your screen.
3. The assistant:
   - Extracts text using OCR
   - Sends it to LLaMA3 via `Ollama` locally
   - Shows answer in a smart popup with action buttons

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/ai-exam-assistant.git
cd ai-exam-assistant
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Install & Run Ollama (if not installed)

Download link
https://ollama.com/download

Run the LLaMA3 model(after insatlling and open and run):
```bash
ollama run llama3
```


Now the set up is done
Run the main.py
```bash
python main.py
```

Now press Ctrl + Alt + V to activate the assistant.

Enjoy
