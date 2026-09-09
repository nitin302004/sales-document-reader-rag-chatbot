import os
import logging

import requests
import streamlit as st


def load_file():
    """
    Sales Document Reader frontend.

    Upload PDF, DOCX, or TXT files and process them
    through the FastAPI backend.
    """

    st.set_page_config(
        page_title="Sales Document Reader",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Sales Document Reader & RAG Chatbot")
    st.write(
        "Upload a sales document to extract structured information "
        "or ask questions about uploaded PDF documents."
    )

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    PORT = int(os.getenv("PORT", 8501))

    API_URL = os.getenv(
        "ROOT_URL",
        "http://localhost:8000"
    )

    SALES_URL = f"{API_URL}/sales"
    CHAT_URL = f"{API_URL}/chat"

    logger.info(f"FastAPI ROOT URL: {API_URL}")
    logger.info(f"SALES URL: {SALES_URL}")
    logger.info(f"CHAT URL: {CHAT_URL}")

    # Session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "results" not in st.session_state:
        st.session_state.results = {}

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # File uploader
    input_file = st.file_uploader(
        "Upload a sales document",
        type=["pdf", "docx", "txt"]
    )

    if input_file is not None:

        if input_file.name not in st.session_state.results:

            st.session_state.messages.append(
                {
                    "content": f"Uploaded {input_file.name}",
                    "is_user": True
                }
            )

            with st.spinner("Processing sales document..."):

                files = {
                    "file": (
                        input_file.name,
                        input_file.getvalue(),
                        input_file.type
                    )
                }

                try:
                    response = requests.post(
                        SALES_URL,
                        files=files
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state.results[
                            input_file.name
                        ] = result

                    else:

                        st.error(
                            f"Error processing file: "
                            f"{response.status_code}"
                        )

                        st.error(response.text)

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )

    # Display extracted results
    if st.session_state.results:

        st.write("## 📋 Extracted Sales Data")

        for file_name, result in st.session_state.results.items():

            entities = result.get("entities", {})

            st.write(f"### {file_name}")

            file_type = result.get("file_type")

            if file_type == "docx":

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Order ID:** "
                        f"{entities.get('order_id', 'Not found')}"
                    )

                    st.write(
                        f"**Order Date:** "
                        f"{entities.get('order_date', 'Not found')}"
                    )

                    st.write(
                        f"**Product:** "
                        f"{entities.get('product', 'Not found')}"
                    )

                    st.write(
                        f"**Category:** "
                        f"{entities.get('category', 'Not found')}"
                    )

                    st.write(
                        f"**Seller:** "
                        f"{entities.get('seller', 'Not found')}"
                    )

                    st.write(
                        f"**Customer:** "
                        f"{entities.get('customer', 'Not found')}"
                    )

                with col2:
                    st.write(
                        f"**Quantity:** "
                        f"{entities.get('quantity', 'Not found')}"
                    )

                    st.write(
                        f"**Unit Price:** "
                        f"{entities.get('unit_price', 'Not found')}"
                    )

                    st.write(
                        f"**Discount:** "
                        f"{entities.get('discount', 'Not found')}"
                    )

                    st.write(
                        f"**Revenue:** "
                        f"{entities.get('revenue', 'Not found')}"
                    )

                    st.write(
                        f"**Region:** "
                        f"{entities.get('region', 'Not found')}"
                    )

                    st.write(
                        f"**Sales Channel:** "
                        f"{entities.get('sales_channel', 'Not found')}"
                    )

            elif file_type == "txt":

                st.write(
                    f"**Order ID:** "
                    f"{entities.get('ORDER_ID', 'Not found')}"
                )

                st.write(
                    f"**Product:** "
                    f"{entities.get('PRODUCT', 'Not found')}"
                )

                st.write(
                    f"**Category:** "
                    f"{entities.get('CATEGORY', 'Not found')}"
                )

                st.write(
                    f"**Seller:** "
                    f"{entities.get('SELLER', 'Not found')}"
                )

                st.write(
                    f"**Quantity:** "
                    f"{entities.get('QUANTITY', 'Not found')}"
                )

                st.write(
                    f"**Unit Price:** "
                    f"{entities.get('UNIT_PRICE', 'Not found')}"
                )

                st.write(
                    f"**Discount:** "
                    f"{entities.get('DISCOUNT', 'Not found')}"
                )

                st.write(
                    f"**Revenue:** "
                    f"{entities.get('REVENUE', 'Not found')}"
                )

                st.write(
                    f"**Region:** "
                    f"{entities.get('REGION', 'Not found')}"
                )

                st.write(
                    f"**Sales Channel:** "
                    f"{entities.get('SALES_CHANNEL', 'Not found')}"
                )

            elif file_type == "pdf":

                st.write(
                    "PDF uploaded successfully and "
                    "stored in the vector database."
                )

                st.json(entities)

                st.write("## 💬 Ask Questions")

                question = st.text_input(
                    "Ask a question about the sales document",
                    key=f"user_input_{file_name}"
                )

                if question:

                    payload = {
                        "question": question
                    }

                    try:

                        response = requests.post(
                            CHAT_URL,
                            json=payload
                        )

                        response.raise_for_status()

                        chat_result = response.json()

                        answer = chat_result.get(
                            "answer",
                            chat_result.get(
                                "answers",
                                "No answer returned."
                            )
                        )

                        st.session_state.chat_history.append(
                            {
                                "role": "user",
                                "message": question
                            }
                        )

                        st.session_state.chat_history.append(
                            {
                                "role": "system",
                                "message": answer
                            }
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Error calling FastAPI: {e}"
                        )

                if st.session_state.chat_history:

                    st.write("### Chat History")

                    for chat in st.session_state.chat_history:

                        if chat["role"] == "user":

                            st.write(
                                f"**You:** {chat['message']}"
                            )

                        else:

                            st.write(
                                f"**Assistant:** {chat['message']}"
                            )



if __name__ == "__main__":
    load_file()
