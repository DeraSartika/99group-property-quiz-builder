# 99 Group - AI Property Quiz Builder

An AI-powered employee learning application designed to help 99 Group employees improve their knowledge of the property industry through interactive quizzes.

## Project Overview

The AI Property Quiz Builder allows employees to generate and complete property-related knowledge assessments. It uses Groq to generate customized multiple-choice questions and provides automatic scoring, answer explanations, and learning points.

The application is built with Python and Streamlit.

## Key Features

- Employee name input
- Custom property topic selection
- Multiple quiz difficulty levels: Beginner, Intermediate, and Advanced
- Quiz generation with 5 or 10 questions in AI Mode
- Four multiple-choice options per question
- Automatic answer evaluation and scoring
- Detailed answer explanations
- Practical learning points
- Downloadable quiz results in JSON format
- Demo Mode that works without an Groq API key
- AI Mode powered by the Groq API

## Technology Stack

- Python
- Streamlit
- Groq API (AI-powered quiz generation)
- OpenAI Python SDK (Groq API-compatible client)
- python-dotenv (environment variable management)
- JSON (quiz data structure and export format)

## Project Structure

```text
99group-property-quiz-builder/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── prompts/
│   └── quiz_generation_prompt.md
└── sample_data/
    └── sample_quiz.json
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/DeraSartika/99group-property-quiz-builder.git
cd 99group-property-quiz-builder
```

Replace `USERNAME` with your GitHub username.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Application Modes

### Demo Mode

Demo Mode uses five predefined sample questions stored in `sample_data/sample_quiz.json`.

No Groq API key is required.

### AI Mode

AI Mode generates customized quizzes using the Groq API.

To enable AI Mode:

1. Copy `.env.example` and rename the copy to `.env`.
2. Open `.env`.
3. Replace the placeholder with your actual Groq API key.
4. Save the file.

Example:

```env
GROQ_API_KEY=your_actual_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Never upload your `.env` file or expose your API key publicly.

## Quiz Workflow

1. Enter the employee name.
2. Enter a property-related topic.
3. Select the number of questions.
4. Choose the difficulty level.
5. Select Demo Mode or AI Mode.
6. Generate the quiz.
7. Answer all multiple-choice questions.
8. Submit the answers.
9. Review the score, explanations, and learning points.
10. Download the quiz results as a JSON file.

## AI Prompt Documentation

The AI quiz-generation instructions and prompt template are documented in:

`prompts/quiz_generation_prompt.md`

## Sample Data

The predefined sample quiz is available in:

`sample_data/sample_quiz.json`

## Limitations and Future Improvements

This project is an educational prototype.

Potential future improvements include:

- Employee authentication
- Quiz history and database integration
- Administrative dashboard
- Employee performance analytics
- Additional quiz categories
- Subject-matter expert review and verified reference sources
- More comprehensive error handling and automated testing

AI-generated content should be reviewed by a subject-matter expert before being used for formal employee assessments.

## Project Purpose

This project demonstrates how generative AI can support employee learning and knowledge assessment within the property industry.

Developed as a prototype project for 99 Group.