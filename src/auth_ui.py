
import streamlit as st

from src.auth import register_user, authenticate_user


def render_auth_page():

    if "auth_mode_next" in st.session_state:
        st.session_state["auth_mode"] = (
            st.session_state.pop("auth_mode_next")
    )
    # AUTHENTICATION PAGE STYLING

    st.markdown(
        """
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 50% 0%,
                    #101B35 0%,
                    #090F1F 50%,
                    #070B16 100%
                );
        }

        .auth-logo {
            text-align: center;
            font-size: 42px;
            margin-top: 35px;
            margin-bottom: 5px;
        }

        .auth-title {
            text-align: center;
            color: #F1F5F9;
            font-size: 32px;
            font-weight: 750;
            letter-spacing: -0.8px;
            margin-bottom: 8px;
        }

        .auth-subtitle {
            text-align: center;
            color: #94A3B8;
            font-size: 14px;
            margin-bottom: 28px;
        }

        [class*="st-key-auth_card"] {
            background: rgba(17, 29, 50, 0.88);
            border: 1px solid #294365;
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
        }

        [class*="st-key-auth_card"] label {
            color: #CBD5E1 !important;
        }

        [class*="st-key-auth_card"] input {
            background: #0B1425 !important;
            color: #F1F5F9 !important;
            border: 1px solid #294365 !important;
            border-radius: 10px !important;
        }

        [class*="st-key-auth_card"] input:focus {
            border-color: #22D3EE !important;
            box-shadow: 0 0 10px rgba(34, 211, 238, 0.12);
        }

        [class*="st-key-auth_card"] button[kind="primaryFormSubmit"] {
            background: linear-gradient(
                135deg,
                #2563EB,
                #0891B2
            ) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 650 !important;
            min-height: 43px;
        }

        [class*="st-key-auth_card"] button[kind="primaryFormSubmit"]:hover {
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2);
        }

        [data-testid="stSegmentedControl"] {
            background: #0B1425;
            border: 1px solid #294365;
            border-radius: 10px;
            padding: 4px;
        }

        [data-testid="stSegmentedControl"] button {
            color: #CBD5E1;
        }

        [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
            background: linear-gradient(
                135deg,
                #2563EB,
                #0891B2
            ) !important;
            color: white !important;
        }

        .auth-footer {
            text-align: center;
            color: #64748B;
            font-size: 11px;
            margin-top: 22px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # CENTER AUTHENTICATION CARD

    left, center, right = st.columns([1, 1.15, 1])

    with center:

        st.markdown(
            """
            <div class="auth-logo">📚</div>

            <div class="auth-title">
                StudyMate AI
            </div>

            <div class="auth-subtitle">
                Your personal AI-powered study companion.
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(
            border=True,
            key="auth_card"
        ):

            # LOGIN / SIGNUP SELECTOR

            auth_mode = st.segmented_control(
                "Authentication",
                options=["Login", "Sign Up"],
                default="Login",
                label_visibility="collapsed",
                width="stretch",
                key="auth_mode"
            )

            st.write("")

            # LOGIN PAGE

            if auth_mode == "Login":

                st.markdown("### Welcome Back 👋")

                st.caption(
                    "Log in to continue your learning journey."
                )

                with st.form("login_form"):

                    email = st.text_input(
                        "Email Address",
                        placeholder="Enter your email"
                    )

                    password = st.text_input(
                        "Password",
                        placeholder="Enter your password",
                        type="password"
                    )

                    login_clicked = st.form_submit_button(
                        "Login",
                        use_container_width=True
                    )

                    if login_clicked:

                        if not email.strip() or not password:

                            st.error(
                                "Please enter your email and password."
                            )

                        else:

                            user = authenticate_user(
                                email,
                                password
                            )

                            if user:

                                st.session_state.authenticated_user = user

                                st.session_state.auth_notice = user
                                st.rerun()

                            else:

                                st.error(
                                    "Invalid email or password."
                                )

            # SIGNUP PAGE

            elif auth_mode == "Sign Up":

                st.markdown("### Create Your Account ✨")

                st.caption(
                    "Join StudyMate AI and organize your learning."
                )

                with st.form("signup_form"):

                    name = st.text_input(
                        "Full Name",
                        placeholder="Enter your full name"
                    )

                    email = st.text_input(
                        "Email Address",
                        placeholder="Enter your email"
                    )

                    password = st.text_input(
                        "Password",
                        placeholder="Create a password",
                        type="password"
                    )

                    confirm_password = st.text_input(
                        "Confirm Password",
                        placeholder="Re-enter your password",
                        type="password"
                    )

                    signup_clicked = st.form_submit_button(
                        "Create Account",
                        use_container_width=True
                    )

                    if signup_clicked:

                        if not all([
                            name.strip(),
                            email.strip(),
                            password,
                            confirm_password
                        ]):

                            st.error(
                                "Please fill in all the fields."
                            )

                        elif password != confirm_password:

                            st.error(
                                "Passwords do not match."
                            )

                        else:

                            try:

                                register_user(
                                    name,
                                    email,
                                    password
                                )

                                st.session_state.auth_notice = (
                                    "Account created successfully! "
                                    "Please log in."
                                )

                                st.session_state.auth_mode_next = "Login"

                                st.rerun()

                            except ValueError as error:

                                st.error(str(error))

        st.markdown(
            """
            <div class="auth-footer">
                ✦ Learn smarter. Stay organized. Grow faster.
            </div>
            """,
            unsafe_allow_html=True
        )

    # DISPLAY SUCCESS NOTICE AFTER RERUN

    if st.session_state.get("auth_notice"):

        st.success(st.session_state.auth_notice)

        del st.session_state.auth_notice
