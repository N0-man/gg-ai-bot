from ollama._client import Client
import os
import gradio as gr

ENGLISH = "English"
MATH = "Math"
RESEARCH = "Research"
DEFAULT_LEARNER = "Hoorain"


class GudduGuide:
    def __init__(self):
        self.ollama_client = Client(host=os.environ.get("OLLAMA_HOST"))

    def prompt(self, name, context):
        def learners_name(name):
            if name is None or name.strip() == "":
                return DEFAULT_LEARNER
            else:
                return name

        if context == MATH:
            return f"""
            You are a math teacher named "Guddu Guide," dedicated to helping a 11-year-old homeschooled child named {learners_name(name)} enhance her problem-solving and critical thinking skills in math. Your approach involves guiding her through math concepts while she learns from Khan Academy and Beast Academy. Rather than providing direct answers, your role is to engage her with thought-provoking questions, encouraging her to think deeply and explore solutions on her own. Additionally, you can provide feedback on her responses, confirming whether she is correct or suggesting improvements if she isn't. You are strictly focused on math topics, so refrain from addressing questions related to English, science, geography, or any general knowledge topics outside of math. Your responses should be structured in the format of a friendly conversation.
            Here’s the context for your interaction:
            - Child's current math lesson topic: 
            - Specific problem or question she is working on: 
            - Areas she needs more help with (if applicable): 

            As you guide her, remember to include follow-up questions that prompt her to reason through the problems, such as:
            - What do you think might be the first step to solving this?
            - Can you explain your thinking behind that answer?
            - How could you check if your answer makes sense?

            Start the conversation now, engaging in a friendly dialogue to help the child think critically about her math problem.
            """
        elif context == RESEARCH:
            return f"""
            You’re an experienced General Knowledge teacher known as "Guddu Guide," specializing in assisting an 11-year-old homeschool learner named who needs to conduct research and prepare a presentation on a specific topic. Your goal is to guide the learner effectively, helping them understand the various concepts in a way that is engaging and easy to grasp.
            Your task is to assist the learner in researching and preparing their presentation.
            As you provide the guidance, keep in mind the following details: - The learner’s current understanding of the topic is at a basic level, so explanations should be simple. - Use analogies and examples that are relatable and age-appropriate to capture their interest. - Encourage critical thinking by asking questions that prompt further exploration of the topic.

            As you guide the learner, please prioritize content from the following resources: National Geographic, PBS KIDS, Fact Monster, Climate Kids, BrainPop, Kiddle, Smithsonian Learning Lab, Wikipedia, MetKids, Funbrain, Kidtopia, Britannica School, History Channel, NASA Kids' Club, KidzSearch, Science Bob, ABCmouse, BBC History for Kids, and How Stuff Works.
            Keep in mind to provide article links and references for the learner to read and explore further. Also, illustrate how you would break down one complex topic into simpler parts for easier understanding to serve as an example for the learner.

            Feel free to engage with the learner by asking them about their research topic.
            Also ensure you dont provide direct answers to math questions.
            """
        else:
            return f"""
            You’re an experienced English teacher known as "Guddu Guide," specializing in assisting an 11-year-old homeschool learner named {learners_name(name)} with improving their English grammar and vocabulary. Your goal is to create a supportive and encouraging environment where the learner feels comfortable learning and making mistakes.
            Your task is to help the learner understand and improve their writing by summarizing mistakes and suggesting better ways of structuring sentences with proper grammar. You will also provide a variety of English words to enhance their vocabulary. 
            Remember, you are not allowed to answer questions related to science, math, geography, or any general knowledge topics except English. 
            Keep the conversation interactive by asking follow-up questions that encourage the learner to express themselves in English. 
            Ensure your responses are short and non-verbose, and make sure to appreciate {learners_name(name)}'s efforts at the end of each exchange to boost their confidence.
            """

    def generate_response(self, message, history, name, context):
        formatted_history = []
        ASSISTANT = "assistant"
        USER = "user"

        def add_context(role, content):
            formatted_history.append({"role": role, "content": content})

        add_context(ASSISTANT, self.prompt(name, context))

        if history and len(history) > 0:
            for user, assistant in history[-10:]:
                add_context(USER, user)
                add_context(ASSISTANT, assistant)

        add_context(USER, message)

        try:
            response = self.ollama_client.chat(
                model="llama3.1",
                messages=formatted_history,
                stream=True,
            )

            partial_message = ""
            for chunk in response:
                if chunk["message"]["content"] is not None:
                    partial_message = partial_message + chunk["message"]["content"]
                    yield partial_message
        except Exception as e:
            raise gr.Error(
                "Guddu guide might be sleeping 💤🛌 Ask daddy to shake-it-up 🐣!",
                duration=10,
            )

    def chatbot(self, name, state):
        return gr.ChatInterface(
            self.generate_response,
            additional_inputs=[name, state],
            chatbot=gr.Chatbot(label="Guddu Guide", height=500),
            textbox=gr.Textbox(
                placeholder="You can ask me anything", container=False, scale=7
            ),
            retry_btn=None,
            undo_btn=None,
            clear_btn=None,
        )


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
        # Your Guddu Guide 🐥
        """
        )
        gr.Markdown(
            """
        There is no end to education. It is not that you read a book, pass an exam and finish with education. The whole of life, from the moment you are born to the moment you die, is a process of learning.
        """
        )
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=100):
                gr.Image(
                    "gg-tiny.png",
                    height=100,
                    width=100,
                    show_label=False,
                    show_download_button=False,
                    container=False,
                    show_fullscreen_button=False,
                )
            with gr.Column(scale=4, min_width=200):
                name_textbox = gr.Textbox(
                    placeholder="add your name if you are not Hoorain",
                    label=f"Hi there...",
                )

        with gr.Tabs(visible=True, selected=ENGLISH):
            with gr.Tab(ENGLISH, id=ENGLISH) as english:
                state = gr.State(ENGLISH)
                _ = ggai.chatbot(name_textbox, state)
            with gr.Tab(MATH, id=MATH) as math:
                state = gr.State(MATH)
                _ = ggai.chatbot(name_textbox, state)
            with gr.Tab(RESEARCH, id=RESEARCH) as research:
                state = gr.State(RESEARCH)
                _ = ggai.chatbot(name_textbox, state)
            with gr.Tab("Why?", id="about") as about:
                gr.Markdown(
                    """
                Why this app?
                # English

                # Math

                # Research
                """
                )

    try:
        ggbot.launch(show_error=True)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
