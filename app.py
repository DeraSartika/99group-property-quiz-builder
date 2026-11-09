
import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ==================================================
# 1. APPLICATION CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="99 Group - AI Property Quiz Builder",
    page_icon="🏠",
    layout="centered"
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = BASE_DIR / "sample_data" / "sample_quiz.json"


def get_api_key():
    """Read the OpenAI API key from environment or Streamlit secrets."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            api_key = None

    return api_key


def get_model():
    """Read the configured OpenAI model."""
    model = os.getenv("GROQ_MODEL")

    if not model:
        try:
            model = st.secrets.get(
                "GROQ_MODEL",
                "openai/gpt-oss-120b"
            )
        except Exception:
            model = "openai/gpt-oss-120b"

    return model


# ==================================================
# 2. LOAD AND VALIDATE QUIZ DATA
# ==================================================

def validate_quiz(quiz, expected_count=None):
    """Check whether generated quiz data follows the required structure."""

    if not isinstance(quiz, dict):
        raise ValueError("Quiz data must be a JSON object.")

    required_fields = ["title", "topic", "difficulty", "questions"]

    for field in required_fields:
        if field not in quiz:
            raise ValueError(f"Missing required field: {field}")

    questions = quiz["questions"]

    if not isinstance(questions, list) or not questions:
        raise ValueError("The quiz must contain questions.")

    if expected_count and len(questions) != expected_count:
        raise ValueError(
            f"Expected {expected_count} questions, "
            f"but received {len(questions)}."
        )

    for index, question in enumerate(questions):
        required_question_fields = [
            "question",
            "options",
            "correct_index",
            "explanation",
            "learning_point"
        ]

        for field in required_question_fields:
            if field not in question:
                raise ValueError(
                    f"Question {index + 1} is missing {field}."
                )

        options = question["options"]
        correct_index = question["correct_index"]

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"Question {index + 1} must have exactly four options."
            )

        if not all(
            isinstance(option, str) and option.strip()
            for option in options
        ):
            raise ValueError(
                f"Question {index + 1} has an invalid option."
            )

        if not isinstance(correct_index, int) or isinstance(
            correct_index, bool
        ):
            raise ValueError(
                f"Question {index + 1} has an invalid answer index."
            )

        if correct_index not in range(4):
            raise ValueError(
                f"Question {index + 1} answer index must be 0 to 3."
            )

        if len(set(options)) != 4:
            raise ValueError(
                f"Question {index + 1} contains duplicate options."
            )

    return quiz


def load_demo_quiz():
    """Load the five-question sample quiz."""

    with open(SAMPLE_FILE, "r", encoding="utf-8") as file:
        quiz = json.load(file)

    return validate_quiz(quiz)


# ==================================================
# 3. AI QUIZ GENERATION
# ==================================================

def generate_ai_quiz(topic, question_count, difficulty):
    """Generate a property-industry quiz using OpenAI."""

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "OpenAI API key was not found. "
            "Please configure your .env file or Streamlit secrets."
        )

    model = get_model()
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1")

    system_prompt = """
You are an instructional designer and property-industry
training specialist creating educational quizzes for 99 Group employees.

Generate accurate, clear, and educational multiple-choice questions.

Return ONLY a valid JSON object using this structure:

{
  "title": "Short quiz title",
  "topic": "Quiz topic",
  "difficulty": "Beginner",
  "questions": [
    {
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_index": 0,
      "explanation": "Explanation of the correct answer.",
      "learning_point": "One practical learning takeaway."
    }
  ]
}

Rules:
- Generate exactly the requested number of questions.
- Every question must have exactly four distinct options.
- Only one option must be clearly correct.
- correct_index must be an integer from 0 to 3.
- Match the requested difficulty level.
- Avoid ambiguous wording and duplicate questions.
- Make questions relevant to property professionals.
- Do not invent statistics, property prices, interest rates,
  regulations, or current market information.
- Explain why each correct answer is right.
- Include one practical learning point per question.
- Use clear and professional language.
"""

    user_prompt = f"""
Create a {difficulty} quiz with exactly {question_count}
multiple-choice questions.

Topic: {topic}

Audience: 99 Group employees working in or supporting
the property industry.

Return only the JSON object using the required structure.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.4
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The AI returned an empty response.")

    quiz = json.loads(content)

    return validate_quiz(
        quiz,
        expected_count=question_count
    )


# ==================================================
# 4. APPLICATION HEADER
# ==================================================

st.title("🏠 99 Group")
st.subheader("AI Property Quiz Builder")

st.write(
    "An AI-powered learning tool designed to help "
    "99 Group employees improve their property-industry knowledge."
)

st.divider()

st.info(
    "Choose Demo Mode to try the sample quiz without an API key, "
    "or AI Mode to generate a customized quiz."
)


# ==================================================
# 5. QUIZ GENERATION FORM
# ==================================================

st.header("Create Your Quiz")

with st.form("quiz_generation_form"):

    employee_name = st.text_input(
        "Employee Name",
        placeholder="Enter your name"
    )

    topic = st.text_input(
        "Property Topic",
        value="Property Market Knowledge in Jakarta",
        help="Enter the property-related topic you want to learn."
    )

    question_count = st.selectbox(
        "Number of Questions",
        options=[5, 10]
    )

    difficulty = st.selectbox(
        "Difficulty Level",
        options=["Beginner", "Intermediate", "Advanced"]
    )

    mode = st.radio(
        "Generation Mode",
        options=["Demo Mode", "AI Mode"],
        horizontal=True
    )

    submitted = st.form_submit_button(
        "Generate Quiz",
        type="primary",
        use_container_width=True
    )


if submitted:

    if not employee_name.strip():
        st.error("Please enter your employee name.")

    elif not topic.strip():
        st.error("Please enter a property topic.")

    else:
        try:
            with st.spinner("Preparing your quiz..."):

                if mode == "Demo Mode":
                    quiz = load_demo_quiz()

                else:
                    quiz = generate_ai_quiz(
                        topic=topic.strip(),
                        question_count=question_count,
                        difficulty=difficulty
                    )

                st.session_state.quiz = quiz
                st.session_state.employee_name = employee_name.strip()
                st.session_state.quiz_mode = mode
                st.session_state.quiz_submitted = False
                st.session_state.quiz_result = None

            st.success("Your quiz is ready!")

        except Exception as error:
            st.error(f"Unable to generate quiz: {error}")


# ==================================================
# 6. DISPLAY QUIZ QUESTIONS
# ==================================================

if "quiz" in st.session_state:

    quiz = st.session_state.quiz

    st.divider()
    st.header(quiz["title"])

    st.write(f"**Employee:** {st.session_state.employee_name}")
    st.write(f"**Topic:** {quiz['topic']}")
    st.write(f"**Difficulty:** {quiz['difficulty']}")
    st.write(f"**Mode:** {st.session_state.quiz_mode}")

    if st.session_state.quiz_mode == "Demo Mode":
        st.caption(
            "Demo Mode uses five predefined sample questions. "
            "The selected question count applies to AI Mode."
        )

    with st.form("quiz_answer_form"):

        selected_answers = []

        for index, question in enumerate(quiz["questions"]):

            st.markdown(
                f"**Question {index + 1}. "
                f"{question['question']}**"
            )

            answer = st.radio(
                "Choose your answer:",
                options=range(4),
                format_func=lambda x: question["options"][x],
                key=f"question_{index}",
                index=None
            )

            selected_answers.append(answer)

            st.divider()

        submitted_answers = st.form_submit_button(
            "Submit Answers",
            type="primary",
            use_container_width=True
        )

    if submitted_answers:

        unanswered = [
            index + 1
            for index, answer in enumerate(selected_answers)
            if answer is None
        ]

        if unanswered:
            st.warning(
                "Please answer all questions before submitting. "
                f"Unanswered questions: {unanswered}"
            )

        else:
            correct_count = 0
            answer_details = []

            for index, question in enumerate(quiz["questions"]):

                selected = selected_answers[index]
                correct = question["correct_index"]
                is_correct = selected == correct

                if is_correct:
                    correct_count += 1

                answer_details.append({
                    "question": question["question"],
                    "selected_answer": question["options"][selected],
                    "correct_answer": question["options"][correct],
                    "is_correct": is_correct,
                    "explanation": question["explanation"],
                    "learning_point": question["learning_point"]
                })

            total_questions = len(quiz["questions"])
            score = round(
                (correct_count / total_questions) * 100
            )

            st.session_state.quiz_result = {
                "employee_name": st.session_state.employee_name,
                "quiz_title": quiz["title"],
                "topic": quiz["topic"],
                "difficulty": quiz["difficulty"],
                "mode": st.session_state.quiz_mode,
                "correct_answers": correct_count,
                "total_questions": total_questions,
                "score": score,
                "answers": answer_details
            }

            st.session_state.quiz_submitted = True


# ==================================================
# 7. RESULTS AND LEARNING REVIEW
# ==================================================

if (
    st.session_state.get("quiz_submitted")
    and st.session_state.get("quiz_result")
):

    result = st.session_state.quiz_result

    st.divider()
    st.header("Quiz Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Final Score",
        f"{result['score']}%"
    )

    col2.metric(
        "Correct Answers",
        f"{result['correct_answers']}/{result['total_questions']}"
    )

    col3.metric(
        "Difficulty",
        result["difficulty"]
    )

    if result["score"] >= 80:
        st.success("Excellent work! You have a strong understanding.")

    elif result["score"] >= 60:
        st.info("Good effort! Keep improving your knowledge.")

    else:
        st.warning(
            "Keep learning! Review the explanations below."
        )

    st.subheader("Answer Review")

    for index, answer in enumerate(result["answers"]):

        st.markdown(f"**Question {index + 1}**")
        st.write(answer["question"])

        if answer["is_correct"]:
            st.success(
                f"Correct: {answer['selected_answer']}"
            )
        else:
            st.error(
                f"Your answer: {answer['selected_answer']}"
            )
            st.write(
                f"Correct answer: {answer['correct_answer']}"
            )

        st.write(f"**Explanation:** {answer['explanation']}")
        st.write(f"**Learning Point:** {answer['learning_point']}")

        st.divider()

    st.subheader("Download Your Results")

    result_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        label="Download Results (JSON)",
        data=result_json,
        file_name="property_quiz_results.json",
        mime="application/json",
        use_container_width=True
    )

    if st.button("Create Another Quiz"):
        for key in [
            "quiz",
            "employee_name",
            "quiz_mode",
            "quiz_submitted",
            "quiz_result"
        ]:
            st.session_state.pop(key, None)

        st.rerun()


# ==================================================
# 8. FOOTER
# ==================================================

st.divider()

st.caption(
    "99 Group - AI Property Quiz Builder | "
    "Educational prototype for employee learning."
)

st.caption(
    "AI-generated content should be reviewed by a "
    "subject-matter expert before formal assessment."
)
