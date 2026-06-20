import streamlit as st
import random

st.set_page_config(
    page_title="Cyber Hangman",
    page_icon="🎮",
    layout="centered"
)

# ---------- CYBER STYLE ----------
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#0B1020,#131A33);
}

.title{
    text-align:center;
    font-size:52px;
    font-weight:bold;
    color:#00FFFF;
    text-shadow:0 0 15px #00FFFF;
}

.score{
    text-align:center;
    color:#00FF99;
    font-size:24px;
    font-weight:bold;
}

.word{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:white;
    letter-spacing:12px;
    padding:20px;
}

.info{
    text-align:center;
    font-size:22px;
    color:#FFD700;
}
</style>
""", unsafe_allow_html=True)

# ---------- WORDS ----------
WORDS = {
    "Easy": [
        "APPLE",
        "HOUSE",
        "TABLE",
        "MUSIC",
        "TIGER"
    ],
    "Medium": [
        "PYTHON",
        "SCIENCE",
        "LAPTOP",
        "NETWORK",
        "GAMING"
    ],
    "Hard": [
        "PROGRAMMING",
        "DEVELOPMENT",
        "CYBERSECURITY",
        "INTELLIGENCE"
    ]
}

# ---------- STATE ----------
if "score" not in st.session_state:
    st.session_state.score = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "word" not in st.session_state:
    st.session_state.word = random.choice(
        WORDS["Easy"]
    )

if "guessed" not in st.session_state:
    st.session_state.guessed = []

if "lives" not in st.session_state:
    st.session_state.lives = 6

# ---------- NEW GAME ----------
def new_game():

    st.session_state.word = random.choice(
        WORDS[st.session_state.difficulty]
    )

    st.session_state.guessed = []

    st.session_state.lives = 6

# ---------- HEADER ----------
st.markdown(
    '<div class="title">⚔️ CYBER HANGMAN ⚔️</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="score">🏆 Score: {st.session_state.score}</div>',
    unsafe_allow_html=True
)

# ---------- DIFFICULTY ----------
difficulty = st.selectbox(
    "🎯 Difficulty",
    ["Easy","Medium","Hard"],
    index=["Easy","Medium","Hard"].index(
        st.session_state.difficulty
    )
)

if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    new_game()

# ---------- NEW GAME BUTTON ----------
if st.button("🔄 New Game"):
    new_game()
    st.rerun()

# ---------- WORD DISPLAY ----------
display = ""

for char in st.session_state.word:

    if char in st.session_state.guessed:
        display += char + " "
    else:
        display += "_ "

st.markdown(
    f'<div class="word">{display}</div>',
    unsafe_allow_html=True
)

# ---------- STATUS ----------
st.progress(st.session_state.lives / 6)

if st.session_state.lives >= 4:
    st.success(
        f"❤️ Lives Left: {st.session_state.lives}"
    )

elif st.session_state.lives >= 2:
    st.warning(
        f"💛 Lives Left: {st.session_state.lives}"
    )

else:
    st.error(
        f"💀 Lives Left: {st.session_state.lives}"
    )

# ---------- ENTER TO GUESS ----------
with st.form("guess_form"):

    guess = st.text_input(
        "⌨️ Type a letter and press ENTER",
        max_chars=1
    ).upper()

    submitted = st.form_submit_button(
        "Guess"
    )

if submitted and guess:

    if guess.isalpha():

        if guess not in st.session_state.guessed:

            st.session_state.guessed.append(
                guess
            )

            if guess not in st.session_state.word:

                st.session_state.lives -= 1

    st.rerun()

# ---------- GUESSED LETTERS ----------
st.markdown("### 🔤 Used Letters")

if st.session_state.guessed:
    st.write(
        " • ".join(
            sorted(st.session_state.guessed)
        )
    )

# ---------- WIN ----------
won = all(
    letter in st.session_state.guessed
    for letter in st.session_state.word
)

if won:

    st.balloons()

    st.success(
        f"🏆 YOU WIN! Word: {st.session_state.word}"
    )

    st.session_state.score += 10

    if st.button("🎮 Play Again"):
        new_game()
        st.rerun()

# ---------- LOSE ----------
if st.session_state.lives <= 0:

    st.error(
        f"💀 GAME OVER! Word was {st.session_state.word}"
    )

    if st.button("🔄 Try Again"):
        new_game()
        st.rerun()
