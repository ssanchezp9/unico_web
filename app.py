import gradio as gr
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def chat(message, history, conversation_id):
    history = history or []

    if conversation_id is None:
        response = requests.post(f"{API_URL}/conversation", json={"user_input": message})
        data = response.json()
        conversation_id = data["conversation_id"]
        bot_message = data["response"]
    else:
        response = requests.post(f"{API_URL}/conversation/{conversation_id}", json={"user_input": message})
        data = response.json()
        bot_message = data["response"]

    history.append((message, bot_message))
    return history, conversation_id, ""

def start_new_conversation():
    return None, [], ""

with gr.Blocks(theme=gr.themes.Default(), fill_height=True) as demo:
    conversation_id_state = gr.State(None)
    
    with gr.Row(equal_height=True):
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                label="Chatbot",
                layout="panel",
                height=750
            )
            msg = gr.Textbox(
                show_label=False,
                placeholder="Introduce tu mensaje y pulsa Enter",
            )
        with gr.Column(scale=1):
            new_conversation_btn = gr.Button("Nueva Conversación")
            clear = gr.Button("Limpiar")

    msg.submit(chat, [msg, chatbot, conversation_id_state], [chatbot, conversation_id_state, msg])
    clear.click(lambda: ([], None), None, [chatbot, conversation_id_state], queue=False)
    new_conversation_btn.click(start_new_conversation, [], [conversation_id_state, chatbot, msg])

demo.launch()
