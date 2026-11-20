
import streamlit as st
import textwrap

import streamlit.components.v1 as components
from Auth.auth_manager import authenticate_user


def show_login():

    # ==========================================
    # CUSTOM LOGIN PAGE CSS
    # ==========================================

    st.markdown(
        textwrap.dedent("""
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 12% 25%,
                    rgba(99, 102, 241, 0.15),
                    transparent 35%
                ),
                radial-gradient(
                    circle at 90% 80%,
                    rgba(168, 85, 247, 0.12),
                    transparent 35%
                ),
                #080d19 !important;
        }

        .block-container {
            max-width: 1180px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 2rem !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        /* BRAND */
        .login-brand {
            font-size: 25px;
            font-weight: 850;
            color: #ffffff;
            letter-spacing: -1px;
            margin-bottom: 35px;
        }

        .brand-symbol {
            color: #a5b4fc;
            font-size: 30px;
            margin-right: 8px;
        }

        /* LEFT PANEL */
        .hero-panel {
            padding: 50px 25px 35px 5px;
        }

        .hero-badge {
            display: inline-block;
            color: #c4b5fd;
            background: rgba(99,102,241,.13);
            border: 1px solid rgba(129,140,248,.3);
            border-radius: 30px;
            padding: 8px 14px;
            font-size: 11px;
            letter-spacing: 1px;
            margin-bottom: 25px;
        }

        .hero-title {
            font-size: clamp(36px, 4.5vw, 58px);
            line-height: 1.15;
            letter-spacing: -2px;
            font-weight: 850;
            color: #ffffff;
            margin-bottom: 20px;
        }

        .hero-gradient {
            background: linear-gradient(
                90deg,#818cf8,#c084fc,#67e8f9
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-description {
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.9;
            max-width: 480px;
            margin-bottom: 35px;
        }

        .feature-item {
            color: #cbd5e1;
            font-size: 14px;
            padding: 9px 0;
        }

        .feature-icon {
            color: #a5b4fc;
            margin-right: 10px;
        }

        /* LOGIN HEADING */
        .login-heading {
            color: #ffffff;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 8px;
        }

        .login-description {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 25px;
        }

        /* LOGIN FORM CARD */
        [data-testid="stForm"] {
            background: rgba(19, 29, 49, 0.94) !important;
            border: 1px solid #33415e !important;
            border-radius: 22px !important;
            padding: 27px !important;
            box-shadow: 0 15px 50px rgba(0,0,0,.25);
        }

        /* INPUT LABELS */
        [data-testid="stTextInput"] label {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        /* INPUT BOXES */
        [data-testid="stTextInput"] input {
            background: #0c1528 !important;
            color: #ffffff !important;
            border: 1px solid #394967 !important;
            border-radius: 11px !important;
            min-height: 45px !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: #818cf8 !important;
            box-shadow: 0 0 0 2px rgba(99,102,241,.15) !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: #64748b !important;
        }

        /* CHECKBOX */
        [data-testid="stCheckbox"] label {
            color: #94a3b8 !important;
            font-size: 12px !important;
        }

        /* LOGIN BUTTON */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(
                100deg,#6366f1,#8b5cf6,#a855f7
            ) !important;
            color: white !important;
            border: none !important;
            min-height: 47px !important;
            border-radius: 11px !important;
            font-weight: 700 !important;
            transition: .3s ease;
            margin-top: 12px;
        }

        [data-testid="stFormSubmitButton"] button:hover {
            box-shadow: 0 5px 25px rgba(129,140,248,.35);
            transform: translateY(-2px);
        }

        /* SECONDARY BUTTON */
        .stButton > button {
            background: #18243a !important;
            color: #c4b5fd !important;
            border: 1px solid #394967 !important;
            border-radius: 10px !important;
            min-height: 42px;
        }

        /* FOOTER */
        .login-footer {
            text-align: center;
            color: #64748b;
            font-size: 11px;
            margin-top: 25px;
        }

        /* RESPONSIVE */
        @media(max-width: 750px) {

            .hero-panel {
                padding: 10px 5px 30px;
            }

            .hero-title {
                font-size: 38px;
            }

            .login-brand {
                margin-bottom: 15px;
            }

            [data-testid="stForm"] {
                padding: 20px !important;
            }
        }

        </style>
        """),
        unsafe_allow_html=True
    )

    # ==========================================
    # BRAND SECTION
    # ==========================================

    st.markdown(
        textwrap.dedent("""
        <div class="login-brand">
            <span class="brand-symbol">✦</span>
            NeuralDocs AI
        </div>
        """),
        unsafe_allow_html=True
    )

    # ==========================================
    # CREATE TWO COLUMNS
    # ==========================================

    left_col, right_col = st.columns(
        [1.1, 0.9],
        gap="large"
    )

    # ==========================================
    # LEFT SIDE - WELCOME SECTION
    # ==========================================

   
    # LEFT PANEL
    with left_col:

        left_html = """
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

        .hero-panel {
            padding: 45px 20px 35px 5px;
        }

        .hero-badge {
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

        .hero-title {
            font-size: clamp(36px, 4.5vw, 58px);
            line-height: 1.15;
            letter-spacing: -2px;
            font-weight: 850;
            color: #ffffff;
            margin-bottom: 22px;
        }

        .hero-gradient {
            display: inline-block;
            background: linear-gradient(
                90deg, #818cf8, #c084fc, #67e8f9
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-description {
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.9;
            max-width: 470px;
            margin-bottom: 30px;
        }

        .feature-item {
            color: #cbd5e1;
            font-size: 14px;
            padding: 11px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .feature-icon {
            color: #a5b4fc;
            font-size: 18px;
        }

        </style>
        </head>

        <body>

        <div class="hero-panel">

            <div class="hero-badge">
                ✦ YOUR INTELLIGENT RESEARCH SPACE
            </div>

            <div class="hero-title">
                Unlock the power of
                <span class="hero-gradient">
                    knowledge.
                </span>
            </div>

            <div class="hero-description">
                Your personal AI research assistant.
                Upload documents, ask intelligent questions
                and discover insights with the power of
                Retrieval Augmented Generation.
            </div>

            <div class="feature-item">
                <span class="feature-icon">✦</span>
                Intelligent document conversations
            </div>

            <div class="feature-item">
                <span class="feature-icon">✦</span>
                AI-powered research assistance
            </div>

            <div class="feature-item">
                <span class="feature-icon">✦</span>
                Your research, organized in one place
            </div>

        </div>

        </body>
        </html>
        """

        components.html(
            left_html,
            height=510,
            scrolling=False
        )


    # ==========================================
    # RIGHT SIDE - LOGIN FORM
    # ==========================================

    with right_col:

        st.markdown(
            textwrap.dedent("""
            <div class="login-heading">
                Welcome back!
            </div>

            <div class="login-description">
                Sign in to continue your AI research journey.
            </div>
            """),
            unsafe_allow_html=True
        )

        with st.form("neuraldocs_login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            col1, col2 = st.columns(2)

            with col1:
                remember = st.checkbox("Remember me")

            with col2:
                st.markdown(
                    """
                    <div style="
                        text-align:right;
                        color:#a5b4fc;
                        font-size:12px;
                        padding-top:8px;
                    ">
                        Forgot password?
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            submitted = st.form_submit_button(
                "Sign In →",
                use_container_width=True
            )

        # ==========================================
        # LOGIN FORM VALIDATION
        # ==========================================

        
        if submitted:

            if not email.strip() or not password:

                st.warning(
                    "Please enter your email and password."
                )

            elif "@" not in email:

                st.warning(
                    "Please enter a valid email address."
                )

            else:

                user = authenticate_user(
                    email,
                    password
                )

                if user is None:

                    st.error(
                        "Invalid email or password."
                    )

                else:

                    st.session_state["authenticated"] = True

                    st.session_state["user"] = user

                    st.session_state["auth_page"] = "dashboard"

                    st.success(
                        f"Welcome back, {user['full_name']}!"
                    )

                    st.rerun()

        # ==========================================
        # SIGNUP REDIRECT PLACEHOLDER
        # ==========================================

        st.markdown(
            """
            <div style="
                text-align:center;
                color:#64748b;
                font-size:12px;
                margin-top:22px;
            ">
                New to NeuralDocs AI?
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Create an Account",
            use_container_width=True):
            st.session_state["auth_page"] = "signup"
            st.rerun()

        # ==========================================
        # FOOTER
        # ==========================================

        st.markdown(
            """
            <div class="login-footer">
                © 2026 NeuralDocs AI
                · Secure AI Research Platform
            </div>
            """,
            unsafe_allow_html=True
        )
