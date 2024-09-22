# from ollama import Client
from ollama._client import Client
import gradio as gr
import os

ENGLISH_PROMPT = '''
Assume the role of a teacher for a 9 years old homeschool child named "Hoorain" who is learning English.
Your task is to correct her grammar mistakes and help her use better english vocabulary. 
Also summarise her mistakes and share corrections. Dont be verbose.
You are not allowed to answer questions related to science, math, geography, or any general knowledge topics except english.
Please ensure to add more follow up questions to continue the conversation in English.
Appreciate "Hoorain" if her sentences are gramatically correct. Your name is "Guddu Guide"
'''

MATH_PROMPT = '''
Assume the role of a teacher for a 9 years old homeschool child named "Hoorain" who is learning Math from Khan academy and Beast Academy.
Your task is to help her in problem solving and critical thinking skills. 
You should not provide direct answers but help her with questions to think and solve it together.
You are not allowed to answer questions related to english, science, geography, or any general knowledge topics except math.
Please ensure to add more follow up questions to help her explore the answer together with you.
Your name is "Guddu Guide"
'''

PROMPT = ENGLISH_PROMPT

OLLAMA_HOST = os.environ.get('OLLAMA_HOST')
ollama_client = Client(host=OLLAMA_HOST)

def generate_response(message, history):
    formatted_history = []
    ASSISTANT = "assistant"
    USER = "user"

    def add_context(role, content):
        formatted_history.append({"role": role, "content":content})    

    if history is None or len(history) == 0:
        add_context(ASSISTANT, PROMPT)
    elif len(history[-1]) == 2:
        user, assistant = history[-1]
        add_context(ASSISTANT, f"{PROMPT} \n users message: {user} \n assistance response: {assistant}")
    else:
        add_context(ASSISTANT, f"{PROMPT} \n\n {history[-1]}")

    add_context(USER, message)
  
    
    try: 
        response = ollama_client.chat(
            model='llama3.1',
            messages=formatted_history,
            stream=True,
        )

        partial_message = ""
        for chunk in response:
            if chunk['message']['content'] is not None:
                    partial_message = partial_message + chunk['message']['content']
                    yield partial_message
    except Exception as e:
        raise gr.Error("Guddu guide might be sleeping 💤🛌 Ask daddy to shake-it-up 🐣!", duration=10)

def chatbot():
    return gr.ChatInterface(
        generate_response,
        chatbot=gr.Chatbot(
            label="Guddu Guide",
            height=500
        ),
        textbox=gr.Textbox(
            placeholder="You can ask me anything", 
            container=False, 
            scale=7
        ),
        retry_btn=None,
        undo_btn=None,
        clear_btn=None
    )

if __name__ == "__main__":
    ENGLISH = "English Vinglish"
    MATH = "Math Beast"
    RESEARCH = "Research Lah"

    theme = gr.themes.Soft(
        primary_hue="pink",
        secondary_hue="rose",
        neutral_hue="sky",
        text_size="lg",
    )

    with gr.Blocks(theme=theme, fill_height=True) as ggbot:
        gr.Markdown(
        """
        # Your personal guide
          There is no end to education. It is not that your ead a book, pass an exam and finish with education. The whole of life, from the moment you are born to the moment you die, is a process of learning.
        """)
        with gr.Tab(ENGLISH):
            _ = chatbot()
        with gr.Tab(MATH):
            _ = chatbot()
        with gr.Tab(RESEARCH):
            _ = chatbot()
        gr.Image(
                "gg-tiny.png", 
                scale=1, 
                show_label=False, 
                show_download_button=False, 
                container=False, 
                show_fullscreen_button=False
            )

    try:
        ggbot.launch(show_error=True)
    except Exception as e:
        print("An error occurred:", str(e))

