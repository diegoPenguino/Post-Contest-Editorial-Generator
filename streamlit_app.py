import streamlit as st

from app_core import generate_editorial, load_default_inputs, load_environment
from utils.validations import validate_file_size, validate_text_limits


def _load_file_text(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8")


st.set_page_config(
    page_title="Problem Editorial Generator",
    page_icon="editorial",
    layout="wide",
)

st.title("Problem Editorial Generator")
st.caption(
    "Generate a competitive programming editorial from a problem statement and accepted solution."
)

default_problem, default_solution = load_default_inputs()
try:
    config = load_environment()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

MODEL_OPTIONS = {
    "Gemini 3.1 Flash Lite": "gemini-3.1-flash-lite",
    "Gemma 4 26B": "gemma-4-26b-a4b-it",
    "Gemma 4 31B": "gemma-4-31b-it",
}

with st.sidebar:
    st.header("Generation Settings")
    default_model_label = next(
        (label for label, value in MODEL_OPTIONS.items() if value == config["model"]),
        "Gemini 3.1 Flash Lite",
    )
    selected_model_label = st.selectbox(
        "Model",
        options=list(MODEL_OPTIONS.keys()),
        index=list(MODEL_OPTIONS.keys()).index(default_model_label),
    )
    model = MODEL_OPTIONS[selected_model_label]
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

col1, col2 = st.columns(2)
input_errors: list[str] = []

with col1:
    st.subheader("Problem Statement")
    problem_upload = st.file_uploader("Upload problem statement (.txt, .md)", type=["txt", "md"], key="problem_upload")
    if problem_upload is not None:
        for error in validate_file_size(problem_upload.size, "Problem statement file"):
            st.error(error)
            input_errors.append(error)
        problem_statement = _load_file_text(problem_upload)
    else:
        problem_statement = st.text_area("Paste the problem statement", value=default_problem, height=420)

with col2:
    st.subheader("Accepted Solution")
    solution_upload = st.file_uploader(
        "Upload accepted solution (.cpp, .txt, .py)", type=["cpp", "txt", "py"], key="solution_upload"
    )
    if solution_upload is not None:
        for error in validate_file_size(solution_upload.size, "Accepted solution file"):
            st.error(error)
            input_errors.append(error)
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
        input_errors.extend(validate_text_limits(problem_statement, "Problem statement", model=model))
        input_errors.extend(validate_text_limits(solution_code, "Accepted solution", model=model))

        if input_errors:
            for error in input_errors:
                st.error(error)
        else:
            with st.spinner("Generating editorial..."):
                try:
                    final_editorial = generate_editorial(
                        problem_statement=problem_statement,
                        solution_code=solution_code,
                        model=model,
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
