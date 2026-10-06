import streamlit as st
import ollama

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Sports Information Assistant",
    page_icon="🏆",
    layout="wide"
)

# --------------------------------------------------
# SPORTS DATA
# --------------------------------------------------

sports_data = {
    "Cricket": {
        "description": """
Cricket is a bat-and-ball sport played between two teams of eleven players.
The main formats are Test cricket, One Day Internationals (ODIs), and Twenty20
(T20) cricket.
""",

        "history": """
Cricket originated in England and gradually became popular in many countries.
Today, it is one of the most popular sports in countries such as India,
Australia, England, Pakistan, South Africa, New Zealand and Sri Lanka.
Major competitions include the ICC Cricket World Cup, ICC T20 World Cup and
various domestic leagues.
""",

        "matches": """
Important cricket competitions and matches include:
• ICC Cricket World Cup
• ICC T20 World Cup
• ICC Champions Trophy
• Indian Premier League (IPL)
• The Ashes
• International Test, ODI and T20 matches
"""
    },

    "Football": {
        "description": """
Football, also called soccer, is a team sport played between two teams of
eleven players. The objective is to score goals by getting the ball into
the opponent's goal.
""",

        "history": """
Modern football developed in England during the 19th century. The sport
later spread throughout the world and became one of the most popular sports.
FIFA governs international football.
""",

        "matches": """
Important football competitions include:
• FIFA World Cup
• UEFA Champions League
• UEFA European Championship
• English Premier League
• La Liga
• FIFA Club World Cup
"""
    },

    "Basketball": {
        "description": """
Basketball is a team sport played between two teams of five players.
Players score points by throwing the ball through the opponent's basket.
""",

        "history": """
Basketball was invented by James Naismith in 1891 in Springfield,
Massachusetts. The sport became popular internationally and is now played
professionally in many countries.
""",

        "matches": """
Important basketball competitions include:
• NBA
• FIBA Basketball World Cup
• Olympic Basketball
• NCAA Basketball
• EuroLeague
"""
    },

    "Tennis": {
        "description": """
Tennis is a racket sport played between two individuals in singles or
two teams of two players in doubles. Players hit a ball over a net.
""",

        "history": """
Modern lawn tennis developed in England during the 19th century.
Tennis has become a major international sport with professional tours
for men and women.
""",

        "matches": """
Important tennis tournaments include:
• Australian Open
• French Open
• Wimbledon
• US Open
• ATP Finals
• WTA Finals
"""
    }
}

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🏆 AI Sports Assistant")

st.sidebar.write("Select a sport:")

selected_sport = st.sidebar.selectbox(
    "Choose Game",
    list(sports_data.keys())
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Powered by Streamlit + Ollama + Llama 3.2:3B"
)

# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------

st.title("🏆 AI Sports Information Assistant")

st.write(
    f"Explore information about **{selected_sport}** and ask questions "
    "using the AI assistant."
)

# --------------------------------------------------
# TABS
# --------------------------------------------------

info_tab, qa_tab = st.tabs(["📖 Info", "🤖 Q&A"])

# ==================================================
# INFO TAB
# ==================================================

with info_tab:

    st.header(f"🏅 {selected_sport}")

    st.subheader("📌 Basic Description")

    st.write(
        sports_data[selected_sport]["description"]
    )

    st.subheader("📜 History")

    st.write(
        sports_data[selected_sport]["history"]
    )

    st.subheader("🏟️ Important / Present Competitions")

    st.write(
        sports_data[selected_sport]["matches"]
    )

# ==================================================
# Q&A TAB
# ==================================================

with qa_tab:

    st.header(f"🤖 Ask AI About {selected_sport}")

    st.write(
        f"Ask any question related to **{selected_sport}**."
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_question = st.chat_input(
        f"Ask something about {selected_sport}..."
    )

    if user_question:

        # Display user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        # AI prompt
        prompt = f"""
You are an AI Sports Information Assistant.

The selected sport is: {selected_sport}.

Answer the user's question about {selected_sport}.

IMPORTANT:
- Give a very short answer.
- Answer in 4 to 5 sentences.
- Use simple English.
- Do not give unnecessary details.
- Do not repeat the question.
- If a list is needed, give maximum 3 points.

User question:
{user_question}
"""

        # Generate response using Ollama
        with st.chat_message("assistant"):

            with st.spinner("AI is thinking..."):

                try:

                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role": "system",
                                "content": prompt
                            },
                            {
                                "role": "user",
                                "content": user_question
                            }
                        ]
                    )

                    answer = response["message"]["content"]

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(
                        "Could not connect to Ollama. "
                        "Make sure Ollama is running and "
                        "llama3.2:3b is installed."
                    )