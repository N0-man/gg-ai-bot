import ollama
import gradio as gr

def generate_response(message, history):
    formatted_history = []
    for user, assistant in history:
        formatted_history.append({"role": "user", "content": user })
        formatted_history.append({"role": "assistant", "content":assistant})

    formatted_history.append({"role": "user", "content": message})
  
    response = ollama.chat(
        model='llama3.1',
        messages=formatted_history,
        stream=True,
    )

    partial_message = ""
    for chunk in response:
        if chunk['message']['content'] is not None:
              partial_message = partial_message + chunk['message']['content']
              yield partial_message

gr.ChatInterface(generate_response,
    chatbot=gr.Chatbot(height=500),
    textbox=gr.Textbox(placeholder="You can ask me anything", container=False, scale=7),
    title="Guddu Guide",
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear").launch()
gr.ChatInterface(generate_response).launch()