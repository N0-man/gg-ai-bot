import ollama
import gradio as gr

def generate_response(message, history):
    formatted_history = []

    if history is None or len(history) == 0:
        formatted_history.append({"role": "user", "content": ENGLISH_USER_PROMPT })
        formatted_history.append({"role": "assistant", "content":ENGLISH_SYS_PROMPT})

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

def chatbot(context):
    return gr.ChatInterface(
        generate_response,
        chatbot=gr.Chatbot(
            height=500
        ),
        textbox=gr.Textbox(
            placeholder="You can ask me anything", 
            container=False, 
            scale=7
        ),
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear"
    )


ENGLISH = "English Vinglish"
MATH = "Math Beast"
RESEARCH = "Research Lah"

ENGLISH_SYS_PROMPT = '''
Assume the role of a teacher for a 9 years old homeschool child named "abc" who is learning English.
Your task is to correct her grammar mistakes during conversation. Please summarise her mistakes and share corrections.
You do not know science, math, geography, or general knowledge, so do not answer these questions.
Please ensure to add more follow up questions to continue the conversation.
appreciate "abc" if her sentences are gramatically correct
'''

ENGLISH_USER_PROMPT = '''
A 9 years old homeschool child learning english
'''


with gr.Blocks() as ggbot:
    with gr.Row(equal_height=False):
        with gr.Column(scale=2, ): 
            _ = gr.Image("gg-tiny.png", scale=1)
        with gr.Column(scale=4, ): 
            with gr.Tab(ENGLISH):
                _ = chatbot(ENGLISH)
            with gr.Tab(MATH):
                _ = chatbot(MATH)

if __name__ == "__main__":
    ggbot.launch()
