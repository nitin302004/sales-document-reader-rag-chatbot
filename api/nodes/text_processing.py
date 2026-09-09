import json
import re

from langchain_core.messages import AIMessage
from api.utils.state import State


def extract_value(text: str, field_name: str):
    """
    Extract the complete value after FIELD:
    Example:
    PRODUCT: Apple MacBook Air M4
    -> Apple MacBook Air M4
    """

    pattern = rf"(?im)^\s*{re.escape(field_name)}\s*[:|]\s*(.+?)\s*$"
    match = re.search(pattern, text)

    return match.group(1).strip() if match else None


def extract_number(text: str, field_name: str):
    """
    Extract numeric values while allowing commas and currency symbols.
    """

    value = extract_value(text, field_name)

    if not value:
        return None

    match = re.search(r"[\d,]+(?:\.\d+)?", value)

    return match.group(0).replace(",", "") if match else None


def extract_percentage(text: str, field_name: str):
    """
    Extract percentage values.
    """

    value = extract_value(text, field_name)

    if not value:
        return None

    match = re.search(r"\d+(?:\.\d+)?%", value)

    return match.group(0) if match else None


def text_processing(state: State) -> State:
    """
    Process a sales-related TXT document and extract
    structured sales information using rule-based extraction.
    """

    print("Started processing the sales TXT file...")

    file_bytes = state["contents"]
    text = file_bytes.decode("utf-8")

    entities = {
        "ORDER_ID": extract_value(text, "ORDER_ID"),
        "PRODUCT": extract_value(text, "PRODUCT"),
        "CATEGORY": extract_value(text, "CATEGORY"),
        "SELLER": extract_value(text, "SELLER"),
        "QUANTITY": extract_number(text, "QUANTITY"),
        "UNIT_PRICE": extract_number(text, "UNIT_PRICE"),
        "DISCOUNT": extract_percentage(text, "DISCOUNT"),
        "REVENUE": extract_number(text, "REVENUE"),
        "REGION": extract_value(text, "REGION"),
        "SALES_CHANNEL": extract_value(text, "SALES_CHANNEL"),
    }

    result = {
        "file_type": "txt",
        "entities": entities
    }

    json_result = json.dumps(result, indent=2)

    response_message = AIMessage(content=json_result)

    state["messages"].append(response_message)

    print("Extracted sales entities:")
    print(json.dumps(entities, indent=2))

    print("Finished processing the sales TXT file...")

    return state
