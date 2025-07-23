import tiktoken
from typing import Union, List, Dict

def count_tokens(text: Union[str, List[Dict[str, str]]], model: str = "gpt-4o") -> int:
    """
    Count the number of tokens in a text string using OpenAI's tokenizer.
    """
    if isinstance(text, list):
        text = " ".join(str(item.get("content", "")) for item in text)
    
    encoder = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoder.encode(text)
    
    return len(tokens)
