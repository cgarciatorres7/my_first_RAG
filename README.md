# My First RAG

A Retrieval-Augmented Generation (RAG) application that allows users to search and interact with YouTube video content. This project uses Streamlit for the web interface and implements various AI/ML components for video processing and question answering.

## Features

- YouTube video search and selection
- Video content processing and analysis
- Interactive question answering about video content
- Modern web interface built with Streamlit

## Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/my_first_RAG.git
cd my_first_RAG
```

2. Create and activate a virtual environment:
```bash
poetry install   # On Windows, use `env\Scripts\activate`
```


## Configuration

1. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the interface to:
   - Search and select YouTube videos
   - Process video content
   - Ask questions about the video content

## Project Structure

```
my_first_RAG/
├── app.py                # Entry point for Streamlit app
├── main.py               # CLI-based main logic for video QA
├── Dockerfile            # Container configuration
├── config/               # Configuration files (e.g., secrets, environment)
├── data/                 # Downloaded videos, processed audio, etc.
├── notebooks/            # Experimentation and prototyping notebooks
├── pages/                # Additional Streamlit app pages
└── src/                  # Core source code
    ├── embedding.py      # Video/audio embedding & preprocessing logic
    ├── generation.py     # Generation & RAG completion logic
    └── retriever.py      # Pinecone query and retrieval utilities
├── poetry.lock
└── pyproject.toml 
```


## Development

- The project uses Streamlit for the web interface
- Video processing is handled using pytubefix and pydub
- AI/ML components use OpenAI and sentence-transformers
- Vector storage is managed with Pinecone

## License

[Add your chosen license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 