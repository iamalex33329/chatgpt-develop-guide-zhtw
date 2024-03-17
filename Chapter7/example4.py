from Chapter7 import func_table
from Chapter7 import chat

import gradio as gr
import openai
import ApiKey

openai.api_key = ApiKey.OPENAI_API_KEY

# openai.Image.create(
#     prompt='',
#     n=1,
#     size='1024x1024'
# )


def txt_to_img_url(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='1024x1024')
    url = response['data'][0]['url']
    return f'![{prompt}]({url})'


func_table.append(
    {
        "chain": False,  # 生圖後不需要傳回給 API
        "func": txt_to_img_url,
        "spec": {
            "name": "txt_to_img_url",
            "description": "由文字生圖並傳回圖像網址",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "描述要產生圖像內容的文字",
                    }
                },
                "required": ["prompt"],
            },
        }
    }
)

messages = []


def wrapper_chat_bot(sys_msg, user_msg, stream):
    messages.append([user_msg, ''])
    for chunk in chat(sys_msg, user_msg, stream):
        messages[-1][1] += chunk
        yield messages


web_chat = gr.Interface(
    fn=wrapper_chat_bot,
    inputs=[
        gr.Textbox(label='System', value='Assistance'),
        gr.Textbox(label='User'),
        gr.Checkbox(label='Streaming', value=False)
    ],
    outputs=[gr.Chatbot(label='AI: ')]
)

web_chat.queue()
web_chat.launch(share=True)
