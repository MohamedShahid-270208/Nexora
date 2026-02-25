# Nexora – AI Adaptive Learning System

An intelligent quiz generator that transforms static notes into adaptive self-assessment.

## Problem Statement
Students often study passively from notes without identifying weak areas. There is no quick way to convert notes into interactive self-assessment tools.

## Solution
Nexora generates quizzes from uploaded notes and analyzes user performance to identify weak topics for targeted practice.

## Features
- Upload .txt notes
- AI-generated quiz from uploaded content
- Score tracking system
- Weak topic detection
- Practice weak topics separately
- Graceful handling of empty or invalid files

## Tech Stack
- Python
- Flask
- HTML
- CSS
- JavaScript

## Project Structure
```
Nexora/
│
├── backend.py
├── templates/
├── static/
├── requirements.txt
└── README.md
```

## How to Run
```
git clone <repo-link>
cd Nexora
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python backend.py
```

## Future Scope
- Support for PDF and DOCX uploads
- User authentication and progress tracking
- Integration with advanced NLP models for improved question generation
