import streamlit as st

from app_core import generate_editorial, load_default_inputs


def _load_file_text(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8")


st.set_page_config(
    page_title="Post-Contest Editorial Generator",
    page_icon="editorial",
    layout="wide",
)

st.title("Post-Contest Editorial Generator")
st.caption(
    "Generate a competitive programming editorial from a problem statement and accepted solution."
)

default_problem, default_solution = load_default_inputs()

with st.sidebar:
    st.header("Generation Settings")
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Problem Statement")
    problem_upload = st.file_uploader("Upload problem statement (.txt)", type=["txt"], key="problem_upload")
    if problem_upload is not None:
        problem_statement = _load_file_text(problem_upload)
    else:
        problem_statement = st.text_area("Paste the problem statement", value=default_problem, height=420)

with col2:
    st.subheader("Accepted Solution")
    solution_upload = st.file_uploader(
        "Upload accepted solution (.cpp, .txt, .py)", type=["cpp", "txt", "py"], key="solution_upload"
    )
    if solution_upload is not None:
        solution_code = _load_file_text(solution_upload)
    else:
        solution_code = st.text_area("Paste the accepted solution", value=default_solution, height=420)

generate_clicked = st.button("Generate Editorial", type="primary", use_container_width=True)

if generate_clicked:
    if not problem_statement.strip():
        st.error("Please provide a problem statement.")
    elif not solution_code.strip():
        st.error("Please provide a solution.")
    else:
        with st.spinner("Generating editorial..."):
            try:
                final_editorial = generate_editorial(
                    problem_statement=problem_statement,
                    solution_code=solution_code,
                    model="gpt-5-nano",
                    temperature=temperature,
                    save_output=False,
                )
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
            else:
                st.success("Editorial generated successfully.")
                st.subheader("Preview")
                st.markdown(final_editorial)
                st.download_button(
                    "Download Markdown",
                    data=final_editorial,
                    file_name="editorial.md",
                    mime="text/markdown",
                )
