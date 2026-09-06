import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom header styling
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E88E5;
            margin-bottom: 0px;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #6c757d;
            margin-bottom: 25px;
        }
    </style>
    <div>
        <p class="main-header">✉️ AI Email Generator</p>
        <p class="sub-header">Your Email Partner</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# API Key handling
groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not groq_api_key:
    with st.sidebar:
        st.subheader("Configuration")
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your free key from https://console.groq.com",
        )

# Form container
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        recipient = st.text_input(
            "Recipient",
            placeholder="e.g., Hiring Manager, Client, Team",
            help="Who will be receiving this email?",
        )
        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Casual",
                "Persuasive",
                "Urgent & Direct",
                "Warm & Friendly",
            ],
        )

    with col2:
        purpose = st.text_input(
            "Goal / Subject Intent",
            placeholder="e.g., Follow up after interview",
            help="What is the primary objective of this message?",
        )
        length = st.selectbox(
            "Email Length",
            ["Short & Concise (2-3 sentences)", "Standard", "Detailed"],
        )

    key_points = st.text_area(
        "Key Points to Include",
        placeholder="- Met yesterday at 2 PM\n- Discussed Q3 roadmap\n- Attached proposal file",
        height=120,
    )

    generate_btn = st.button("Generate Email ✨", type="primary", use_container_width=True)

# Generation logic
if generate_btn:
    if not groq_api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not purpose or not key_points:
        st.warning("Please fill in both the goal and key points.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            prompt = f"""
            Write an email with these guidelines:
            - Recipient: {recipient}
            - Main Goal: {purpose}
            - Desired Tone: {tone}
            - Length: {length}
            - Key Details: {key_points}

            Formatting requirements:
            - Provide a clear, compelling Subject line at the top.
            - Follow with a well-structured Email Body.
            - Use standard business placeholders like [Your Name] where appropriate.
            """

            with st.spinner("Drafting your email..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert executive communication assistant that writes polished, ready-to-send emails.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                )

            email_content = response.choices[0].message.content

            st.success("Draft ready!")
            with st.container(border=True):
                st.markdown(email_content)

        except Exception as e:
        
            st.error(f"Error: {e}")