from ollama._client import Client
import os
import gradio as gr
from dataclasses import dataclass


ENGLISH = "English"
MATH = "Math"
RESEARCH = "Research"
DEFAULT_LEARNER = "Hoorain"

class GudduGuide:
    def __init__(self):
        self.learners_name = "HOORAIN"
        self.english = "English"
        self.math = "Math"
        self.research = "Research"
        self.__context = self.english
        self.ollama_client = Client(host=os.environ.get('OLLAMA_HOST'))

    def prompt(name, context):
        # if self.__context == self.math:
        if context == MATH:
            return f'''
            Assume the role of a teacher for a 9 years old homeschool child named {name} who is learning Math from Khan academy and Beast Academy.
            Your task is to help her in problem solving and critical thinking skills. 
            You should not provide direct answers but help her with questions to think about the answers.
            You are allowed to provide if her answer is correct or wrong.
            You are not allowed to answer questions related to english, science, geography, or any general knowledge topics except math.
            Please ensure to add more follow up questions to help her explore the answer.
            Your name is "Guddu Guide".
            '''
        else: 
            return f'''
            Assume the role of a teacher for a 9 years old homeschool child named {name} who is learning English.
            Your task is to correct her grammar mistakes and help her use better english vocabulary. 
            Also summarise her mistakes and share corrections. Dont be verbose.
            You are not allowed to answer questions related to science, math, geography, or any general knowledge topics except english.
            Please ensure to add more follow up questions to continue the conversation in English.
            Appreciate {name} if her sentences are gramatically correct. Your name is "Guddu Guide"
            '''

    def generate_response(self, message, history, name, context):
        formatted_history = []
        ASSISTANT = "assistant"
        USER = "user"

        def add_context(role, content):
            formatted_history.append({"role": role, "content":content})

        def learners_name():
            if name is None or name.strip() == "":
                return "Hoorain"
            else:
                return name

        add_context(ASSISTANT, self.prompt(name, context))

        if history and len(history) > 0:
            for user, assistant in history[-10:]:
                add_context(USER, user)
                add_context(ASSISTANT, assistant)

        add_context(USER, message)
        
        try: 
            response = self.ollama_client.chat(
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

    def chatbot(self, name, context):
        return gr.ChatInterface(
            self.generate_response,
            additional_inputs=[name, context],
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
    
    # def change_learners_name(self, name):
    #     if name is None or name.strip() == "":
    #         self.learners_name = "Hoorain"
    #     else:
    #         self.learners_name = name

    # def change_context(self, context, context_textbox):
    #     self.__context = context
    #     context_textbox.value = context

def main():
    theme = gr.themes.Soft(
        primary_hue="pink",
        secondary_hue="rose",
        neutral_hue="sky",
        text_size="lg",
    )
    ggai = GudduGuide()

    with gr.Blocks(theme=theme, fill_height=True) as ggbot:
        gr.Markdown(
        """
        # Your personal guide
          There is no end to education. It is not that your ead a book, pass an exam and finish with education. The whole of life, from the moment you are born to the moment you die, is a process of learning.
        """)
        with gr.Row():
            with gr.Column():
                name_textbox = gr.Textbox(placeholder="add your name if you are not Hoorain", label=f"Hi there...")
            with gr.Column():
                context = gr.Dropdown(["English", "Math", "Research"], info="What can I help you with?", show_label=False)

        with gr.Tabs(visible=True, selected=ggai.english): 
            with gr.Tab(ggai.english, id=ggai.english) as english:
                _ = ggai.chatbot(name_textbox, context)
            with gr.Tab(ggai.math, id=ggai.math) as math:
                _ = ggai.chatbot(name_textbox, context)
            with gr.Tab(ggai.research, id=ggai.research) as research:
                _ = ggai.chatbot(name_textbox, context)
            with gr.Tab("Why?", id="about") as about:
                gr.Markdown(
                """
                # English

                # Math

                # Research
                """)
        gr.Image(
                "gg-tiny.png", 
                scale=1, 
                show_label=False, 
                show_download_button=False, 
                container=False, 
                show_fullscreen_button=False
            )
        # name_textbox.change(ggai.change_learners_name, name_textbox)
        # english.select(lambda :ggai.change_context(ggai.english, context_label), None)
        # math.select(lambda :ggai.change_context(ggai.math, context_label), None)
        # research.select(lambda :ggai.change_context(ggai.research, context_label), None)
        # about.select(lambda :ggai.change_context(ggai.english, context_label), None)
    try:
        ggbot.launch(show_error=True)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()