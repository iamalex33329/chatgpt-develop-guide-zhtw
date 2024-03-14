import gradio as gr

from Chapter7 import chat


def wrapper_chat(sys_msg, user_msg, stream):
    reply = ''
    for chunk in chat(sys_msg, user_msg, stream):
        reply += chunk
        yield reply


web_chat = gr.Interface(
    fn=wrapper_chat,
    inputs=['text', 'text', 'checkbox'],
    outputs=['text']
)

web_chat.queue()
web_chat.launch(share=True)