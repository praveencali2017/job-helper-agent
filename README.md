# Job Helper Agent

An LLM-powered career assistant that reads your CV, looks up job postings, and tells you how well you fit each role, with suggestions for improving your CV.

It is built as a LangGraph ReAct agent. The agent can call two kinds of tools:

- **CV text extraction:** reads a local PDF or DOCX CV.
- **Job posting lookup:** uses the OpenAI Responses API with web search to fetch a job posting URL and summarise it (title, company, salary, requirements, and so on).

## Project structure

The tools follow a ports-and-adapters layout, so an implementation (for example the PDF library or the LLM provider) can be swapped without touching the services or the agent.

```
config/             Settings loaded from environment / .env (pydantic-settings)
prompt_templates/   System and user prompts for the job-posting lookup
services/           Services that wrap the tools and expose them to LangChain (as_tools)
tools/
  ports/            Abstract interfaces (TextExtractor, LLMWebSearch)
  adapters/         Concrete implementations (pdfplumber, python-docx, OpenAI web search)
builder.ipynb       Notebook that builds and runs the LangGraph agent
```

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key

## Setup

```bash
uv sync
```

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=sk-...
```

`.env` is git-ignored. A real `OPENAI_API_KEY` environment variable overrides the value in `.env`.

## Usage

Start Jupyter and open `builder.ipynb`:

```bash
uv run jupyter lab
```

The notebook:

1. Builds the text-extraction and job-posting services.
2. Wraps them as LangChain tools and binds them to the chat model.
3. Compiles a ReAct graph (assistant ⇄ tools).
4. Runs it with a question such as *"Here is my CV at `cv-template.pdf` and three job links. Which role suits me best?"*

`cv-template.pdf` is a sample CV you can use for testing.

## Limitations

- **Job boards may block automated access.** Indeed and similar sites often block bots, so a lookup can come back as "Job posting unavailable". When that happens, paste the job description text instead, or use postings hosted on Greenhouse, Lever, or company career pages.
- **Every lookup costs money.** Each job URL triggers a separate OpenAI web-search call.
