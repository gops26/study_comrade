# Study Comrade

Study Comrade is an AI-powered assistant that helps you interact with PDF documents using natural language. Upload your PDFs, ask questions, and get accurate answers powered by LLMs and vector search.

## Features

- Upload PDF files and process them for semantic search
- Ask questions about your uploaded documents
- Uses [LangChain](https://github.com/langchain-ai/langchain), [Gradio](https://gradio.app/), and [ChromaDB](https://www.trychroma.com/)
- Embeddings via HuggingFace models
- LLM responses via Groq API

## Project Structure

```
.env
requirements.txt
src/
    __init__.py
    app.py
    main.py
    utils/
        utils.py
    config/
        app_config.yml
    data/
        vectordb/
            processed/
                chroma/
    uploads/
        files/
```

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Edit the `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   HUGGING_FACE=your_huggingface_api_key
   tavily_api_key=your_tavily_api_key
   ```

4. **Run the app**
   ```sh
   cd src
   python app.py
   ```

   The Gradio interface will launch in your browser.

## Usage

- Upload a PDF using the interface.
- Ask questions about the content of the PDF.
- View answers and chat history.

## Configuration

Modify `src/config/app_config.yml` to change model settings, directories, and chunking parameters.


## License

MIT License

---

**Note:** This project uses third-party APIs and models. Ensure you comply with their terms of service.
