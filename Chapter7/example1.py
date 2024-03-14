import gradio as gr

from Chapter7 import chat

web_chat = gr.Interface(
    fn=chat,
    inputs=['text', 'text'],
    outputs=['text']
)

web_chat.queue()
web_chat.launch(share=True)
