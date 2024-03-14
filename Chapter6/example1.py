import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY


def get_reply(messages, stream=False):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=stream
        )

        if stream:
            # In streaming mode, use a helper function to obtain complete text
            for res in response:
                if 'content' in res['choices'][0]['delta']:
                    yield res['choices'][0]['delta']['content']
        else:
            # In non-streaming mode, directly yield the complete reply text
            yield response['choices'][0]['message']['content']

    except openai.OpenAIError as err:
        # Handle OpenAI errors
        reply = f"An {err.error.type} error occurred\n{err.error.message}"
        print(reply)
        yield reply


# Non-Streaming
for reply in get_reply([{'role': 'user', 'content': 'how are you'}]):
    print(reply)

# Streaming
for reply in get_reply([{'role': 'user', 'content': 'how are you'}], stream=True):
    print(reply, end='')
