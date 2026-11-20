
import streamlit as st
import pandas as pd

from Auth.auth_manager import (
    get_all_users,
    get_login_history,
    promote_user_to_admin
)


def show_admin():

    # ==========================================
    # SECURITY CHECK
    # ==========================================

    current_user = st.session_state.get("user", {})

    if (
        not st.session_state.get("authenticated", False)
        or current_user.get("role") != "admin"
    ):
        st.error("Access denied. Admin permission required.")

        if st.button("Back to Chat"):
            st.session_state["app_page"] = "chat"
            st.rerun()

        return

    # ==========================================
    # ADMIN DASHBOARD CSS
    # ==========================================

    st.markdown("""
    <style>
    .admin-title {
        color: #ffffff;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .admin-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .admin-card {
        background: linear-gradient(145deg,#17243a,#101829);
        border: 1px solid #2b3b58;
        border-radius: 15px;
        padding: 20px;
    }

    .admin-card-label {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 10px;
    }

    .admin-card-value {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # HEADER
    # ==========================================

    st.markdown(
        '<div class="admin-title">🛡️ Admin Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="admin-subtitle">'
        'Manage registered users and monitor login activity.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("← Back to AI Chat"):
        st.session_state["app_page"] = "chat"
        st.rerun()

    # ==========================================
    # FETCH DATABASE RECORDS
    # ==========================================

    try:
        users = get_all_users()
        login_history = get_login_history(limit=200)

    except Exception as e:
        st.error(f"Unable to load admin data: {e}")
        return

    total_users = len(users)
    total_admins = sum(
        1 for user in users if user["role"] == "admin"
    )
    total_logins = len(login_history)

    # ==========================================
    # STATISTICS
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="admin-card">
            <div class="admin-card-label">TOTAL REGISTERED USERS</div>
            <div class="admin-card-value">{total_users}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="admin-card">
            <div class="admin-card-label">ADMIN ACCOUNTS</div>
            <div class="admin-card-value">{total_admins}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="admin-card">
            <div class="admin-card-label">RECENT LOGIN RECORDS</div>
            <div class="admin-card-value">{total_logins}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==========================================
    # ADMIN TABS
    # ==========================================

    users_tab, activity_tab, promote_tab = st.tabs([
        "👥 Registered Users",
        "📊 Login Activity",
        "🛡️ Manage Admins"
    ])

    # ==========================================
    # REGISTERED USERS
    # ==========================================

    with users_tab:

        st.subheader("Registered Users")

        if users:

            user_data = []

            for user in users:
                user_data.append({
                    "ID": user["id"],
                    "Full Name": user["full_name"],
                    "Email": user["email"],
                    "Role": user["role"].upper(),
                    "Registered At": user["created_at"],
                    "Last Login": user["last_login"] or "Never"
                })

            st.dataframe(
                pd.DataFrame(user_data),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No registered users found.")

    # ==========================================
    # LOGIN HISTORY
    # ==========================================

    with activity_tab:

        st.subheader("Recent Login Activity")

        if login_history:

            st.dataframe(
                pd.DataFrame(login_history),
                use_container_width=True,
                hide_index=True
            )

            st.caption("Showing up to the latest 200 login records.")

        else:
            st.info("No login activity found.")

    # ==========================================
    # PROMOTE USER TO ADMIN
    # ==========================================

    with promote_tab:

        st.subheader("Promote User to Admin")

        st.warning(
            "Only promote accounts belonging to trusted administrators."
        )

        with st.form("promote_admin_form"):

            admin_email = st.text_input(
                "Registered User Email",
                placeholder="user@example.com"
            )

            submitted = st.form_submit_button(
                "Promote to Admin",
                use_container_width=True
            )

        if submitted:

            if not admin_email.strip():
                st.warning("Please enter an email address.")

            elif promote_user_to_admin(admin_email):

                st.success(
                    "Admin role assigned successfully."
                )

                st.rerun()

            else:
                st.error("No registered user found with this email.")
