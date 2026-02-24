from flask import Flask, request, jsonify, render_template
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_file_path = None

@app.route("/")
def home():
    return render_template("Nexora.html")

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_file_path

    file = request.files.get("file")

    if not file:
        return jsonify({"message": "No file uploaded"}), 400

    if not file.filename.endswith(".txt"):
        return jsonify({"message": "Only .txt files allowed"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    uploaded_file_path = file_path

    return jsonify({"message": "File uploaded successfully"})

import re
@app.route("/ask", methods=["POST"])
def ask():
    global uploaded_file_path

    if not uploaded_file_path:
        return jsonify({"answer": "Please upload a .txt file first."})

    data = request.json
    question = data.get("question", "").lower().strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    with open(uploaded_file_path, "r", encoding="utf-8") as f:
        notes = f.read().lower()


    sentences = re.split(r'[.\n!?]+', notes)

    stop_words = {
        "is", "the", "a", "an", "of", "in", "on",
        "what", "who", "why", "how", "when", "where",
        "and", "to", "for", "with"
    }

    question_words = [
        word for word in re.findall(r'\w+', question)
        if word not in stop_words and len(word) > 2
    ]

    best_sentence = ""
    max_score = 0

    for sentence in sentences:
        score = sum(1 for word in question_words if word in sentence)

        if score > max_score:
            max_score = score
            best_sentence = sentence

    if max_score < 1 or not best_sentence.strip():
        return jsonify({
            "answer": "No strong match found in your notes. This topic might need revision."
        })

    return jsonify({
        "answer": best_sentence.strip().capitalize()
    })
import random
@app.route("/quiz", methods=["GET"])
def quiz():
    global uploaded_file_path

    if not uploaded_file_path:
        return jsonify({"message": "Please upload a .txt file first."})

    with open(uploaded_file_path, "r", encoding="utf-8") as f:
        notes = f.read()

    sentences = re.split(r'[.\n!?]+', notes)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if len(sentences) < 3:
        return jsonify({"message": "Not enough content to generate quiz."})

    MAX_QUESTIONS = 10

    valid_sentences = [s for s in sentences if len(s.split()) > 6]

    selected = random.sample(
        valid_sentences,
        min(MAX_QUESTIONS, len(valid_sentences))
    )

    questions = []

    for sentence in selected:
        words = re.findall(r'\b\w+\b', sentence)

        if len(words) < 6:
            continue

        blank_index = random.randint(1, len(words) - 2)
        correct_answer = words[blank_index]

        words[blank_index] = "_____"
        question_text = " ".join(words)

        topic_words = re.findall(r'\b\w+\b', sentence.lower())
        detected_topic = topic_words[0] if topic_words else "general"

        questions.append({
            "question": question_text,
            "answer": correct_answer,
            "topic": detected_topic
        })
    return jsonify({"quiz": questions})
@app.route("/quiz_weak", methods=["POST"])
def quiz_weak():
    global uploaded_file_path

    data = request.json
    topics = data.get("topics", [])

    if not uploaded_file_path:
        return jsonify({"message": "Upload file first."})

    with open(uploaded_file_path, "r", encoding="utf-8") as f:
        notes = f.read()

    sentences = re.split(r'[.\n!?]+', notes)

    filtered = []

    for sentence in sentences:
        for topic in topics:
            if topic.lower() in sentence.lower():
                filtered.append(sentence)
                break

    if not filtered:
        return jsonify({"message": "No weak-topic content found."})

    selected = random.sample(filtered, min(5, len(filtered)))

    questions = []

    for sentence in selected:
        words = re.findall(r'\b\w+\b', sentence)

        if len(words) < 6:
            continue

        blank_index = random.randint(1, len(words) - 2)
        correct_answer = words[blank_index]

        words[blank_index] = "_____"
        question_text = " ".join(words)

        topic_words = re.findall(r'\b\w+\b', sentence.lower())
        detected_topic = topic_words[0] if topic_words else "general"

        questions.append({
            "question": question_text,
            "answer": correct_answer,
            "topic": detected_topic
        })

    return jsonify({"quiz": questions})
app.run(debug=True)