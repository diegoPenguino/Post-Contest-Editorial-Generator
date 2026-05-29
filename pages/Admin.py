import os

import streamlit as st

from utils import fetch_submissions, get_submission, initialize_database


st.set_page_config(
    page_title="Admin",
    page_icon="lock",
    layout="wide",
)

st.title("Admin")
st.caption("Admin page")

db_path = initialize_database()

admin_password = os.getenv("ADMIN_PASSWORD", "")
if not admin_password:
    st.warning("Set ADMIN_PASSWORD to protect this page.")
    st.stop()

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    with st.form("admin_login"):
        password = st.text_input("Admin password", type="password")
        submitted = st.form_submit_button("Enter admin view", use_container_width=True)

    if submitted:
        if password == admin_password:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()

status_filter = st.selectbox(
    "Status",
    options=["All", "received", "processing", "completed", "failed", "validation_failed"],
    index=0,
)
search_query = st.text_input("Search submissions", placeholder="Search by ID or content")
limit = st.slider("Rows to load", min_value=10, max_value=500, value=20, step=10)

selected_status = None if status_filter == "All" else status_filter
df = fetch_submissions(
    db_path=db_path,
    status=selected_status,
    query=search_query.strip() or None,
    limit=limit,
)

if df.empty:
    st.info("No submissions found yet.")
    st.stop()

summary = {
    "Total": int(df.shape[0]),
    "Completed": int((df["status"] == "completed").sum()),
    "Failed": int((df["status"] == "failed").sum()),
    "Pending": int(df["status"].isin(["received", "processing"]).sum()),
}

metric_cols = st.columns(len(summary))
for col, (label, value) in zip(metric_cols, summary.items()):
    col.metric(label, value)

display_columns = [
    "created_at",
    "updated_at",
    "status",
    "model",
    "temperature",
    "id",
]
st.dataframe(df[display_columns], use_container_width=True, hide_index=True)

st.download_button(
    "Download CSV",
    data=df.to_csv(index=False),
    file_name="submissions.csv",
    mime="text/csv",
    use_container_width=True,
)

st.divider()

selected_id = st.selectbox("Inspect submission", options=df["id"].tolist()) or df["id"].iloc[0]
submission = get_submission(selected_id, db_path=db_path)

if submission:
    detail_left, detail_right = st.columns(2)
    detail_left.write(f"**Created:** {submission['created_at']}")
    detail_left.write(f"**Updated:** {submission['updated_at']}")
    detail_left.write(f"**Status:** {submission['status']}")
    detail_right.write(f"**Model:** {submission['model']}")
    detail_right.write(f"**Temperature:** {submission['temperature']}")
    detail_right.write(f"**Submission ID:** `{submission['id']}`")

    st.subheader("Problem Statement")
    st.text_area(
        "Problem Statement",
        value=submission["problem_statement"],
        height=220,
        label_visibility="collapsed",
        disabled=True,
    )

    st.subheader("Accepted Solution")
    st.text_area(
        "Accepted Solution",
        value=submission["solution_code"],
        height=220,
        label_visibility="collapsed",
        disabled=True,
    )

    st.subheader("Generated Editorial")
    st.text_area(
        "Generated Editorial",
        value=submission["editorial_markdown"] or "",
        height=260,
        label_visibility="collapsed",
        disabled=True,
    )

    if submission["error_message"]:
        st.subheader("Error")
        st.error(submission["error_message"])

    if submission["metadata_json"]:
        st.subheader("Metadata")
        st.code(submission["metadata_json"], language="json")
