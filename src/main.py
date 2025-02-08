import os

import streamlit as st
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerationResponse,
    GenerativeModel,
    Tool,
    grounding,
)

SYSTEM_PROMPT = """
あなたは高度な知識を持つAIアシスタントです．ユーザーの質問に対し，Google検索用のツールを利用して回答します．
公式のURLを参照し，信頼性の高い情報を提供します．
"""


def get_entry_point_html(response) -> str:
    entry_point_html = response.candidates[
        0
    ].grounding_metadata.search_entry_point.rendered_content
    info_entry_point_html = f"#### 検索ワード\n\n{entry_point_html}"
    return info_entry_point_html


def get_citations(response) -> str:
    urls = ""
    for grounding_chunk in response.candidates[0].grounding_metadata.grounding_chunks:
        # print(grounding_chunk)  # 空の可能性あり．
        urls += f"- [{grounding_chunk.web.title}]({grounding_chunk.web.uri})\n"
    info_citations = f"#### 参考URL\n\n{urls}"
    return info_citations


def format_result(response) -> str:
    result_content = response.text
    citations = get_citations(response)
    entry_point_html = get_entry_point_html(response)
    return f"{result_content}\n\n{citations}\n\n{entry_point_html}"


def generate_answer_google_search(
    model: GenerativeModel, prompt: str
) -> GenerationResponse:
    # Use Google Search for grounding
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

    response = model.generate_content(
        prompt,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )
    return response


def display_history(messages) -> None:
    for message in messages:
        display_msg_content(message)


def display_msg_content(message) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"], unsafe_allow_html=True)


@st.cache_resource
def initialize_vertexai() -> None:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertexai-credentials.json"
    vertexai.init()


@st.cache_resource
def get_gc_model() -> GenerativeModel:
    return GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT
    )


def main() -> None:
    initialize_vertexai()
    model = get_gc_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    display_history(st.session_state.messages)

    if prompt := st.chat_input("What's up?"):
        input_msg = {"role": "user", "content": [{"text": prompt}]}
        display_msg_content(input_msg)
        st.session_state.messages.append(input_msg)

        response = generate_answer_google_search(model, prompt)
        formatted_result = format_result(response)
        response_msg = {
            "role": "assistant",
            "content": [{"text": formatted_result}],
        }
        display_msg_content(response_msg)
        st.session_state.messages.append(response_msg)


if __name__ == "__main__":
    main()
