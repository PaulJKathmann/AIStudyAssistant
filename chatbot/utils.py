import tiktoken
#from app import fs


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-1106"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            if isinstance(value, str):
                # Only encode if value is a string
                num_tokens += len(encoding.encode(value))
            else:
                # Handle the case where value is not a string
                # Log an error or take appropriate action
                print(f"Warning: Expected a string for value at: '{key}:{value}', but got {type(value)}")
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

