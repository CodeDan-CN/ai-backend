import tiktoken


def get_num_tokens(model_name: str, text: str):
    if len(text) == 0:
        return 0

    enc = tiktoken.encoding_for_model(model_name)

    tokenized_text = enc.encode(text)

    # calculate the number of tokens in the encoded text
    return len(tokenized_text)

