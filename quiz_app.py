"""
🎓 Machine Learning Exam Revision Quiz
A gamified quiz application for ELEC70137 - Python and Machine Learning
"""

import streamlit as st
import json
import random
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🎓 ML Quiz Master",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Space+Mono&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(120deg, #e94560, #f39c12, #00d9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 20px;
    }
    
    .score-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        font-family: 'Space Mono', monospace;
    }
    
    .score-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .streak-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 15px 25px;
        display: inline-block;
        margin: 10px 5px;
        box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
    }
    
    .streak-text {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .question-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .question-number {
        background: linear-gradient(135deg, #00d9ff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .question-text {
        color: #ffffff;
        font-size: 1.3rem;
        line-height: 1.6;
        margin: 15px 0;
    }
    
    .topic-badge {
        background: rgba(233, 69, 96, 0.2);
        color: #e94560;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid rgba(233, 69, 96, 0.3);
    }
    
    .stRadio > label {
        color: #ffffff !important;
    }
    
    div[data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 10px;
    }
    
    div[data-testid="stRadio"] label {
        color: #e0e0e0 !important;
        font-size: 1.05rem;
        padding: 12px 15px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .correct-answer {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 217, 255, 0.2) 100%);
        border: 2px solid #00ff88;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.2) 0%, rgba(233, 69, 96, 0.2) 100%);
        border: 2px solid #ff4757;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .explanation-box {
        background: rgba(102, 126, 234, 0.15);
        border-left: 4px solid #667eea;
        border-radius: 0 15px 15px 0;
        padding: 20px;
        margin: 15px 0;
        color: #e0e0e0;
    }
    
    .translation-box {
        background: rgba(243, 156, 18, 0.15);
        border-left: 4px solid #f39c12;
        border-radius: 0 15px 15px 0;
        padding: 15px;
        margin: 10px 0;
        color: #e0e0e0;
        font-style: italic;
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 5px;
        margin: 20px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
    }
    
    .final-score-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 3px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2, #e94560) 1;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin: 30px 0;
    }
    
    .achievement-badge {
        font-size: 5rem;
        margin: 20px 0;
    }
    
    .sidebar .stSelectbox label {
        color: #ffffff !important;
    }
    
    .xp-bar {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .xp-fill {
        background: linear-gradient(90deg, #00d9ff, #00ff88);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00d9ff;
        font-family: 'Space Mono', monospace;
    }
    
    .stat-label {
        color: #a0a0a0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .confetti {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# Load questions
@st.cache_data(show_spinner=False)
def load_questions():
    with open('quiz_questions_v4.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Normalize field names: ensure all questions use 'correct' not 'correct_answer'
        for q in data['questions']:
            if 'correct_answer' in q and 'correct' not in q:
                q['correct'] = q['correct_answer']
                del q['correct_answer']
        return data

data = load_questions()
questions = data['questions']

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'max_streak' not in st.session_state:
    st.session_state.max_streak = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 20
if 'answers_history' not in st.session_state:
    st.session_state.answers_history = []
if 'show_translation' not in st.session_state:
    st.session_state.show_translation = False
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1

# XP System
def calculate_xp(correct, streak):
    base_xp = 100 if correct else 10
    streak_bonus = min(streak * 20, 100)
    return base_xp + streak_bonus if correct else base_xp

def get_level(xp):
    return min(xp // 500 + 1, 50)

def get_level_progress(xp):
    return (xp % 500) / 500 * 100

# Get grade based on percentage
def get_grade(percentage):
    if percentage >= 90:
        return "🏆", "A+", "LEGENDARY!", "#FFD700"
    elif percentage >= 80:
        return "🌟", "A", "EXCELLENT!", "#00ff88"
    elif percentage >= 70:
        return "✨", "B", "GREAT JOB!", "#00d9ff"
    elif percentage >= 60:
        return "👍", "C", "GOOD EFFORT!", "#667eea"
    elif percentage >= 50:
        return "📚", "D", "KEEP STUDYING!", "#f39c12"
    else:
        return "💪", "F", "DON'T GIVE UP!", "#e94560"

# Sidebar
with st.sidebar:
    st.markdown('<h2 style="color: #00d9ff; text-align: center;">⚙️ Quiz Settings</h2>', unsafe_allow_html=True)
    
    # Topic filter
    all_topics = sorted(list(set(q['topic'] for q in questions)))
    selected_topics = st.multiselect(
        "📚 Select Topics",
        options=all_topics,
        default=all_topics,
        help="Choose which topics to include"
    )
    
    # Number of questions
    num_questions = st.slider(
        "📝 Number of Questions",
        min_value=10,
        max_value=100,
        value=20,
        step=5
    )
    
    # Shuffle option
    shuffle_questions = st.checkbox("🔀 Shuffle Questions", value=True)
    
    st.markdown("---")
    
    # Stats display
    st.markdown('<h3 style="color: #f39c12;">📊 Your Stats</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stat-item" style="background: rgba(102, 126, 234, 0.2); border-radius: 15px; padding: 15px; margin: 10px 0;">
        <div style="color: #00d9ff; font-size: 1.5rem; font-weight: 700;">Level {st.session_state.level}</div>
        <div style="color: #a0a0a0; font-size: 0.8rem;">CURRENT LEVEL</div>
    </div>
    """, unsafe_allow_html=True)
    
    # XP Progress bar
    progress = get_level_progress(st.session_state.xp)
    st.markdown(f"""
    <div style="color: #a0a0a0; font-size: 0.8rem; margin-bottom: 5px;">XP: {st.session_state.xp} / {(st.session_state.level) * 500}</div>
    <div class="xp-bar">
        <div class="xp-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="display: flex; gap: 10px; margin-top: 15px;">
        <div style="flex: 1; background: rgba(0, 255, 136, 0.2); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="color: #00ff88; font-size: 1.2rem; font-weight: 700;">🔥 {st.session_state.max_streak}</div>
            <div style="color: #a0a0a0; font-size: 0.7rem;">BEST STREAK</div>
        </div>
        <div style="flex: 1; background: rgba(233, 69, 96, 0.2); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="color: #e94560; font-size: 1.2rem; font-weight: 700;">🎯 {st.session_state.score}</div>
            <div style="color: #a0a0a0; font-size: 0.7rem;">TOTAL SCORE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reset button
    if st.button("🔄 Reset Quiz", use_container_width=True):
        for key in ['current_question', 'score', 'streak', 'answered', 'selected_answer', 
                    'show_explanation', 'quiz_started', 'quiz_questions', 'answers_history', 'show_translation']:
            if key in st.session_state:
                if key == 'score':
                    st.session_state[key] = 0
                elif key == 'streak':
                    st.session_state[key] = 0
                elif key in ['answered', 'show_explanation', 'quiz_started', 'show_translation']:
                    st.session_state[key] = False
                elif key in ['quiz_questions', 'answers_history']:
                    st.session_state[key] = []
                else:
                    st.session_state[key] = 0
        st.rerun()

# Main content
st.markdown('<h1 class="main-title">🧠 ML Quiz Master</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Master Machine Learning with Interactive Quizzes | ELEC70137</p>', unsafe_allow_html=True)

# Start screen
if not st.session_state.quiz_started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="question-card" style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🎓</div>
            <h2 style="color: #ffffff; margin-bottom: 15px;">Ready to Test Your Knowledge?</h2>
            <p style="color: #a0a0a0; margin-bottom: 25px;">
                Challenge yourself with 100 carefully crafted questions covering:<br>
                <span style="color: #00d9ff;">Linear Regression • Decision Trees • SVM • K-Means • Random Forests</span><br>
                <span style="color: #f39c12;">Cross-Validation • Regularization • Bias-Variance • And More!</span>
            </p>
            <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 20px 0;">
                <div style="background: rgba(0, 217, 255, 0.2); padding: 15px 25px; border-radius: 15px;">
                    <span style="color: #00d9ff; font-size: 1.5rem; font-weight: 700;">📝 {0}</span>
                    <span style="color: #a0a0a0; display: block; font-size: 0.8rem;">Questions</span>
                </div>
                <div style="background: rgba(0, 255, 136, 0.2); padding: 15px 25px; border-radius: 15px;">
                    <span style="color: #00ff88; font-size: 1.5rem; font-weight: 700;">🎯 {1}</span>
                    <span style="color: #a0a0a0; display: block; font-size: 0.8rem;">Topics</span>
                </div>
                <div style="background: rgba(233, 69, 96, 0.2); padding: 15px 25px; border-radius: 15px;">
                    <span style="color: #e94560; font-size: 1.5rem; font-weight: 700;">🌍 EN/FR</span>
                    <span style="color: #a0a0a0; display: block; font-size: 0.8rem;">Bilingual</span>
                </div>
            </div>
        </div>
        """.format(num_questions, len(selected_topics)), unsafe_allow_html=True)
        
        if st.button("🚀 Start Quiz", use_container_width=True):
            # Filter and select questions
            filtered = [q for q in questions if q['topic'] in selected_topics]
            if shuffle_questions:
                random.shuffle(filtered)
            st.session_state.quiz_questions = filtered[:num_questions]
            st.session_state.total_questions = len(st.session_state.quiz_questions)
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.streak = 0
            st.session_state.answers_history = []
            st.rerun()

# Quiz in progress
elif st.session_state.current_question < len(st.session_state.quiz_questions):
    q = st.session_state.quiz_questions[st.session_state.current_question]

    # Validate question structure
    if not isinstance(q, dict) or 'options' not in q:
        st.error(f"Error: Question at index {st.session_state.current_question} is malformed. Question data: {q}")
        st.stop()

    # Handle both 'correct' and 'correct_answer' field names for compatibility
    if 'correct' not in q and 'correct_answer' not in q:
        st.error(f"Error: Question {q.get('id', 'unknown')} is missing both 'correct' and 'correct_answer' fields.")
        st.stop()

    # Normalize the field name to 'correct' if it's 'correct_answer'
    if 'correct_answer' in q and 'correct' not in q:
        q['correct'] = q['correct_answer']
    
    # Progress bar
    progress = (st.session_state.current_question) / st.session_state.total_questions
    st.markdown(f"""
    <div class="progress-container">
        <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 8px; border-radius: 10px; width: {progress * 100}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.2); border-radius: 15px; padding: 15px; text-align: center;">
            <div style="color: #667eea; font-size: 1.8rem; font-weight: 700;">{st.session_state.current_question + 1}/{st.session_state.total_questions}</div>
            <div style="color: #a0a0a0; font-size: 0.7rem; text-transform: uppercase;">Question</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(0, 255, 136, 0.2); border-radius: 15px; padding: 15px; text-align: center;">
            <div style="color: #00ff88; font-size: 1.8rem; font-weight: 700;">{st.session_state.score}</div>
            <div style="color: #a0a0a0; font-size: 0.7rem; text-transform: uppercase;">Score</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: rgba(243, 156, 18, 0.2); border-radius: 15px; padding: 15px; text-align: center;">
            <div style="color: #f39c12; font-size: 1.8rem; font-weight: 700;">🔥 {st.session_state.streak}</div>
            <div style="color: #a0a0a0; font-size: 0.7rem; text-transform: uppercase;">Streak</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        accuracy = (st.session_state.score / (st.session_state.current_question)) * 100 if st.session_state.current_question > 0 else 0
        st.markdown(f"""
        <div style="background: rgba(233, 69, 96, 0.2); border-radius: 15px; padding: 15px; text-align: center;">
            <div style="color: #e94560; font-size: 1.8rem; font-weight: 700;">{accuracy:.0f}%</div>
            <div style="color: #a0a0a0; font-size: 0.7rem; text-transform: uppercase;">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Question card
    st.markdown(f"""
    <div class="question-card">
        <span class="topic-badge">{q['topic']}</span>
        <div class="question-number">QUESTION {st.session_state.current_question + 1}</div>
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Translation toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.checkbox("🇫🇷 Show French", key="trans_toggle"):
            st.markdown(f"""
            <div class="translation-box">
                <strong>Traduction:</strong> {q['question_fr']}
            </div>
            """, unsafe_allow_html=True)
    
    # Answer options
    if not st.session_state.answered:
        selected = st.radio(
            "Select your answer:",
            options=q['options'],
            index=None,
            key=f"q_{st.session_state.current_question}"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit Answer", use_container_width=True, disabled=selected is None):
                # Validate question has required fields
                if 'correct' not in q:
                    st.error(f"Question {q.get('id', 'unknown')} is missing the 'correct' field. Please check the quiz_questions_v4.json file.")
                    st.stop()

                st.session_state.selected_answer = q['options'].index(selected)
                st.session_state.answered = True

                if st.session_state.selected_answer == q['correct']:
                    st.session_state.score += 1
                    st.session_state.streak += 1
                    st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
                    xp_earned = calculate_xp(True, st.session_state.streak)
                else:
                    st.session_state.streak = 0
                    xp_earned = calculate_xp(False, 0)

                st.session_state.xp += xp_earned
                st.session_state.level = get_level(st.session_state.xp)
                st.session_state.answers_history.append({
                    'question': q['question'],
                    'correct': st.session_state.selected_answer == q['correct'],
                    'your_answer': q['options'][st.session_state.selected_answer],
                    'correct_answer': q['options'][q['correct']]
                })
                st.rerun()
    
    else:
        # Show result
        # Validate question has required fields
        if 'correct' not in q:
            st.error(f"Question {q.get('id', 'unknown')} is missing the 'correct' field. Please check the quiz_questions_v4.json file.")
            st.stop()

        is_correct = st.session_state.selected_answer == q['correct']
        
        if is_correct:
            st.markdown(f"""
            <div class="correct-answer">
                <div style="font-size: 2rem; margin-bottom: 10px;">✅ Correct! +{calculate_xp(True, st.session_state.streak)} XP</div>
                <div style="color: #00ff88; font-size: 1.1rem;">
                    {q['options'][q['correct']]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.session_state.streak >= 3:
                st.balloons()
        else:
            st.markdown(f"""
            <div class="wrong-answer">
                <div style="font-size: 2rem; margin-bottom: 10px;">❌ Incorrect</div>
                <div style="color: #ff4757; margin-bottom: 10px;">
                    Your answer: {q['options'][st.session_state.selected_answer]}
                </div>
                <div style="color: #00ff88;">
                    ✓ Correct answer: {q['options'][q['correct']]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Explanation
        st.markdown(f"""
        <div class="explanation-box">
            <div style="color: #667eea; font-weight: 600; margin-bottom: 10px;">📖 Explanation</div>
            <div style="color: #e0e0e0; line-height: 1.7;">{q['explanation']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # French explanation toggle
        if st.checkbox("🇫🇷 Show French Explanation", key="exp_trans"):
            st.markdown(f"""
            <div class="translation-box">
                <strong>Explication:</strong> {q['explanation_fr']}
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Next Question", use_container_width=True):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.selected_answer = None
                st.rerun()

# Quiz completed
else:
    percentage = (st.session_state.score / st.session_state.total_questions) * 100
    emoji, grade, message, color = get_grade(percentage)
    
    st.markdown(f"""
    <div class="final-score-card">
        <div class="achievement-badge">{emoji}</div>
        <h1 style="color: {color}; font-size: 3rem; margin: 10px 0;">{message}</h1>
        <div style="font-size: 4rem; font-weight: 700; color: white; margin: 20px 0;">
            {st.session_state.score} / {st.session_state.total_questions}
        </div>
        <div style="font-size: 2rem; color: {color}; margin-bottom: 20px;">
            Grade: {grade} ({percentage:.1f}%)
        </div>
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 30px;">
            <div style="text-align: center;">
                <div style="color: #00ff88; font-size: 2rem; font-weight: 700;">🔥 {st.session_state.max_streak}</div>
                <div style="color: #a0a0a0;">Best Streak</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #00d9ff; font-size: 2rem; font-weight: 700;">⭐ {st.session_state.xp}</div>
                <div style="color: #a0a0a0;">Total XP</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #f39c12; font-size: 2rem; font-weight: 700;">🏅 Level {st.session_state.level}</div>
                <div style="color: #a0a0a0;">Your Level</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if percentage >= 70:
        st.balloons()
    
    # Performance by topic
    st.markdown('<h3 style="color: #00d9ff; margin-top: 30px;">📊 Performance by Topic</h3>', unsafe_allow_html=True)
    
    topic_stats = {}
    for i, q in enumerate(st.session_state.quiz_questions):
        topic = q['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}
        topic_stats[topic]['total'] += 1
        if st.session_state.answers_history[i]['correct']:
            topic_stats[topic]['correct'] += 1
    
    cols = st.columns(min(3, len(topic_stats)))
    for i, (topic, stats) in enumerate(topic_stats.items()):
        with cols[i % 3]:
            topic_pct = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
            color = "#00ff88" if topic_pct >= 70 else "#f39c12" if topic_pct >= 50 else "#e94560"
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 15px; margin: 5px 0;">
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 5px;">{topic}</div>
                <div style="color: {color}; font-size: 1.5rem; font-weight: 700;">{stats['correct']}/{stats['total']}</div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 5px; height: 8px; margin-top: 10px;">
                    <div style="background: {color}; height: 100%; border-radius: 5px; width: {topic_pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Review mistakes
    mistakes = [h for h in st.session_state.answers_history if not h['correct']]
    if mistakes:
        st.markdown('<h3 style="color: #e94560; margin-top: 30px;">❌ Questions to Review</h3>', unsafe_allow_html=True)
        for m in mistakes[:5]:
            st.markdown(f"""
            <div style="background: rgba(233, 69, 96, 0.1); border-radius: 15px; padding: 15px; margin: 10px 0; border-left: 4px solid #e94560;">
                <div style="color: #ffffff; margin-bottom: 10px;">{m['question']}</div>
                <div style="color: #e94560; font-size: 0.9rem;">Your answer: {m['your_answer']}</div>
                <div style="color: #00ff88; font-size: 0.9rem;">Correct: {m['correct_answer']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.streak = 0
            st.session_state.answered = False
            st.session_state.answers_history = []
            st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 50px; padding: 20px;">
    <p>🎓 ML Quiz Master | ELEC70137 - Python and Machine Learning</p>
    <p style="font-size: 0.8rem;">Created for exam revision | Imperial College London</p>
</div>
""", unsafe_allow_html=True)
