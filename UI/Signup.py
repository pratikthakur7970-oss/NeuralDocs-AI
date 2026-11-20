
import re
import streamlit as st
import streamlit.components.v1 as components
from Auth.auth_manager import register_user, authenticate_user


def show_signup():

    # ==========================================
    # SIGNUP PAGE STYLING
    # ==========================================

    st.markdown("""
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 12% 25%,
                rgba(99,102,241,.15),
                transparent 35%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(168,85,247,.12),
                transparent 35%
            ),
            #080d19 !important;
    }

    .block-container {
        max-width: 1180px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
    }

    .signup-brand {
        color: white;
        font-size: 25px;
        font-weight: 850;
        letter-spacing: -1px;
        margin-bottom: 30px;
    }

    .signup-symbol {
        color: #a5b4fc;
        font-size: 30px;
        margin-right: 8px;
    }

    .signup-heading {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .signup-description {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 22px;
    }

    [data-testid="stForm"] {
        background: rgba(19,29,49,.94) !important;
        border: 1px solid #33415e !important;
        border-radius: 22px !important;
        padding: 25px !important;
        box-shadow: 0 15px 50px rgba(0,0,0,.25);
    }

    [data-testid="stTextInput"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    [data-testid="stTextInput"] input {
        background: #0c1528 !important;
        color: #ffffff !important;
        border: 1px solid #394967 !important;
        border-radius: 11px !important;
        min-height: 43px !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,.15) !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }

    [data-testid="stCheckbox"] label {
        color: #cbd5e1 !important;
        font-size: 12px !important;
    }

    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(
            100deg,#6366f1,#8b5cf6,#a855f7
        ) !important;
        color: white !important;
        border: none !important;
        min-height: 47px !important;
        border-radius: 11px !important;
        font-weight: 700 !important;
        margin-top: 12px;
        transition: .3s ease;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        box-shadow: 0 5px 25px rgba(129,140,248,.35);
        transform: translateY(-2px);
    }

    .stButton > button {
        background: #18243a !important;
        color: #c4b5fd !important;
        border: 1px solid #394967 !important;
        border-radius: 10px !important;
        min-height: 42px;
    }

    @media(max-width: 750px) {
        .block-container {
            padding-top: 1rem !important;
        }

        [data-testid="stForm"] {
            padding: 18px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # BRAND
    # ==========================================

    st.markdown("""
    <div class="signup-brand">
        <span class="signup-symbol">✦</span>
        NeuralDocs AI
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns(
        [1.1, 0.9],
        gap="large"
    )

    # ==========================================
    # LEFT PANEL
    # ==========================================

    with left_col:

        signup_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }

        .hero {
            padding: 45px 20px 35px 5px;
        }

        .badge {
            display: inline-block;
            color: #c4b5fd;
            background: rgba(99,102,241,.13);
            border: 1px solid rgba(129,140,248,.3);
            border-radius: 30px;
            padding: 9px 15px;
            font-size: 11px;
            letter-spacing: 1px;
            margin-bottom: 28px;
        }

        .title {
            font-size: clamp(36px, 4.5vw, 58px);
            line-height: 1.15;
            font-weight: 850;
            letter-spacing: -2px;
            color: #ffffff;
            margin-bottom: 22px;
        }

        .gradient {
            display: inline-block;
            background: linear-gradient(
                90deg,#818cf8,#c084fc,#67e8f9
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .description {
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.9;
            max-width: 470px;
            margin-bottom: 30px;
        }

        .feature {
            color: #cbd5e1;
            font-size: 14px;
            padding: 11px 0;
        }

        .symbol {
            color: #a5b4fc;
            margin-right: 10px;
        }

        </style>
        </head>

        <body>

        <div class="hero">

            <div class="badge">
                ✦ JOIN THE NEURALDOCS COMMUNITY
            </div>

            <div class="title">
                Start your journey
                <span class="gradient">
                    with AI.
                </span>
            </div>

            <div class="description">
                Create your account and experience
                intelligent document conversations.
                Turn your research into knowledge
                with your personal AI assistant.
            </div>

            <div class="feature">
                <span class="symbol">✦</span>
                Smart document understanding
            </div>

            <div class="feature">
                <span class="symbol">✦</span>
                Intelligent AI conversations
            </div>

            <div class="feature">
                <span class="symbol">✦</span>
                Your personal research workspace
            </div>

        </div>

        </body>
        </html>
        """

        components.html(
            signup_html,
            height=510,
            scrolling=False
        )

    # ==========================================
    # RIGHT PANEL
    # ==========================================

    with right_col:

        st.markdown("""
        <div class="signup-heading">
            Create Account
        </div>

        <div class="signup-description">
            Sign up to get started with NeuralDocs AI.
        </div>
        """, unsafe_allow_html=True)

        with st.form("neuraldocs_signup_form"):

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )

            terms = st.checkbox(
                "I agree to the Terms and Conditions"
            )

            submitted = st.form_submit_button(
                "Create Account →",
                use_container_width=True
            )

        # ==========================================
        # BASIC FORM VALIDATION
        # ==========================================

        
        if submitted:

            if not full_name.strip():

                st.warning(
                    "Please enter your full name."
                )

            elif not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                email.strip()
            ):

                st.warning(
                    "Please enter a valid email address."
                )

            elif len(password) < 8:

                st.warning(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif not terms:

                st.warning(
                    "Please accept the Terms and Conditions."
                )

            else:

                success, message = register_user(
                    full_name,
                    email,
                    password
                )

                if not success:

                    st.error(message)

                else:

                    user = authenticate_user(
                        email,
                        password
                    )

                    if user:

                        st.session_state["authenticated"] = True

                        st.session_state["user"] = user

                        st.session_state["auth_page"] = "dashboard"

                        st.success(
                            "Account created successfully!"
                        )

                        st.rerun()

                    else:

                        st.session_state["auth_page"] = "login"

                        st.success(
                            "Account created. Please sign in."
                        )

                        st.rerun()


        st.markdown("""
        <div style="
            text-align:center;
            color:#64748b;
            font-size:12px;
            margin-top:22px;
        ">
            Already have an account?
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Sign In Instead",
            use_container_width=True,
            key="signup_back_to_login"
        ):
            st.session_state["auth_page"] = "login"
            st.rerun()
