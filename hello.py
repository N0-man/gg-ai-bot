import ollama
import gradio as gr

def chat(msg):
  return 'ok'

with gr.Blocks(
    title='test',
    css=".contain { display: flex !important; flex-direction: column !important; }"
    "#component-0, #component-3, #component-10, #component-8  { height: 100% !important; }"
    "#chatbot { flex-grow: 1 !important; overflow: auto !important;}"
    "#col { height: 100vh !important; }"
) as blocks:
    with gr.Row():
        # gr.HTML("<img src='/gg-tiny.png'")
        gr.Image("gg-tiny.png")
    
    with gr.Row(equal_height=False):
        with gr.Column(scale=3, ): 
            mode = gr.Radio(
                ["English Vinglish", "Math Beast", "Research Lah"],
                label="Mode",
                value="Query Docs",
            )
            upload_button = gr.components.UploadButton(
                "Upload File(s)",
                type="filepath",
                file_count="multiple",
                size="sm",
            )
            ingested_dataset = gr.List(
                headers=["File name"],
                label="Ingested Files",
                interactive=False,
                render=False,  # Rendered under the button
            )
            upload_button.upload(
                inputs=upload_button,
                outputs=ingested_dataset,
            )
            ingested_dataset.change(
                outputs=ingested_dataset,
            )
            ingested_dataset.render()
        with gr.Column(scale=7, elem_id='col'):
            _ = gr.ChatInterface(
                chat,
                chatbot=gr.Chatbot(
                    show_copy_button=True,
                    render=False,
                    elem_id="chatbot",
                )
            )

blocks.launch()