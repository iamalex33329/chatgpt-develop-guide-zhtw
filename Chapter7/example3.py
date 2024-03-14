import gradio as gr

from Chapter7 import chat


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