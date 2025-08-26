import gradio as gr
from main import gradio_wrapper_func, process_pdf
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(placeholder="he", type="messages")
    gr.ChatInterface(
        fn=gradio_wrapper_func,
        title="study comrade",
        chatbot=chatbot,
        type="messages",
        flagging_mode='manual',
        flagging_options=["like", "Spam", "Inappropriate", "Other"],
        save_history=True

    )
    pdf_file = gr.File(label="upload your pdf", file_types=[".pdf"])
    upload_status = gr.Textbox(label="status", interactive=False)
    pdf_file.upload(process_pdf, inputs=pdf_file, outputs=upload_status)


if __name__ == "__main__":
    demo.launch()
