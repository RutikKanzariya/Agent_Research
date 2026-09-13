# 🔎 Agent Research

An AI-powered **multi-agent research system** built with Python and LangChain.

The project automatically researches a given topic by searching the web, extracting detailed information from relevant sources, generating a structured research report, and finally reviewing the report using an AI critic.

---

## 🚀 Overview

**Agent Research** uses multiple AI components to automate the research workflow.

Instead of manually searching multiple websites, reading articles, collecting information, and reviewing the final report, the system performs these steps automatically:

```text
Research Topic
      │
      ▼
┌─────────────────┐
│   Search Agent  │
│  Web Research   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Reader Agent  │
│  URL Scraping   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Writer Chain  │
│ Generate Report │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Critic Chain  │
│ Review & Score  │
└────────┬────────┘
         │
         ▼
   Final Research
      + Feedback
```

The main pipeline is implemented in `pipeline.py`. It creates the search agent, reader agent, writer chain, and critic chain and executes them sequentially.

---

## ✨ Features

* 🤖 Multi-agent AI research workflow
* 🔎 Real-time web search using Tavily
* 🌐 Web page content extraction using BeautifulSoup
* 🧠 LLM-powered research writing
* 📝 Structured research reports
* 🔍 AI-based report criticism and scoring
* 📚 Source URL collection
* 🔗 LangChain agent architecture
* 🌱 Environment variable support using `.env`
* 🐍 Python-based implementation

---

## 🧩 Architecture

The project contains four major AI components.

### 1. Search Agent

The Search Agent searches the web for:

* Recent information
* Reliable sources
* Relevant articles
* Topic-specific information

It uses the custom `web_search` tool powered by Tavily.

---

### 2. Reader Agent

The Reader Agent receives the search results, selects a relevant URL, and extracts deeper information from that webpage.

The project uses:

* `requests`
* `BeautifulSoup`

to retrieve and clean webpage content.

---

### 3. Writer Chain

The Writer Chain combines the search results and scraped content and generates a professional research report.

The generated report contains:

* Introduction
* Key Findings
* Conclusion
* Sources

The writer is implemented using LangChain's Expression Language (LCEL).

---

### 4. Critic Chain

The Critic Chain reviews the generated report and provides:

* Score out of 10
* Strengths
* Areas to improve
* Final verdict

This provides an additional quality-control step after report generation.

---

## 🛠️ Tech Stack

| Technology     | Purpose                    |
| -------------- | -------------------------- |
| Python         | Core programming language  |
| LangChain      | AI agent and LLM framework |
| LangChain Core | Prompts and LCEL chains    |
| Groq           | LLM inference              |
| Llama 3.3 70B  | Language model             |
| Tavily         | Web search                 |
| BeautifulSoup  | Web scraping               |
| Requests       | HTTP requests              |
| python-dotenv  | Environment variables      |
| Pandas         | Data processing            |
| Rich           | Terminal output            |

The repository's dependency list includes LangChain, Google Generative AI support, Tavily, BeautifulSoup, Requests, python-dotenv, Pandas, Rich, Pydantic and other supporting packages.

---

## 📁 Project Structure

```text
Agent_Research/
│
├── app/
│
├── agents.py
├── pipeline.py
├── tools.py
├── main.py
├── listofmodel.py
├── test.py
│
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

### Important Files

#### `agents.py`

Contains:

* Search Agent
* Reader Agent
* Writer Chain
* Critic Chain
* LLM configuration

The project currently uses the Groq `llama-3.3-70b-versatile` model through LangChain.

#### `tools.py`

Contains the custom tools used by the agents:

```text
web_search()
scrape_url()
```

The web search tool uses Tavily, while the scraping tool uses Requests and BeautifulSoup.

#### `pipeline.py`

Controls the complete research workflow:

```text
Search
  ↓
Read
  ↓
Write
  ↓
Critic
```

It exposes:

```python
run_research_pipeline(topic)
```

and can also be executed directly from the terminal.

#### `main.py`

Contains the basic application entry point.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/RutikKanzariya/Agent_Research.git
```

Move into the project directory:

```bash
cd Agent_Research
```

---

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

Using `pip`:

```bash
pip install -r requirements.txt
```

The project also contains `pyproject.toml` and `uv.lock` for Python dependency management.

---

## 🔑 Environment Variables

The project requires API keys for the external AI and search services.

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

If you want to use Google Gemini instead of Groq, configure the appropriate Google API key and model settings in `agents.py`.

### ⚠️ Important

Never commit your `.env` file to GitHub.

Your `.gitignore` already excludes environment files.

For example:

```gitignore
.env
.env.*
!.env.example
```

You can create an `.env.example` file containing placeholders:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## ▶️ Running the Project

Run the research pipeline:

```bash
python pipeline.py
```

The application will ask:

```text
Enter a Research Topic:
```

For example:

```text
Enter a Research Topic: Artificial Intelligence in Healthcare
```

The pipeline will then execute:

```text
Step 1 - Search agent working ...

Step 2 - Reader agent is Scraping top resources ...

Step 3 - Writer is drafting the report ...

Step 4 - Critic is reviewing the report ...
```

The final output contains the generated research report and the critic's evaluation.

---

## 🧪 Example Workflow

### Input

```text
Artificial Intelligence in Healthcare
```

### Search Agent

Finds relevant and recent information from the web.

### Reader Agent

Selects a relevant source and extracts deeper content.

### Writer

Creates a structured report:

```text
Introduction

Key Findings
1. ...
2. ...
3. ...

Conclusion

Sources
- URL 1
- URL 2
```

### Critic

Evaluates the generated report:

```text
Score: 8/10

Strengths:
- Well structured
- Relevant information

Areas to Improve:
- Add more recent sources
- Improve explanation of some findings

One line verdict:
A strong research report with minor areas for improvement.
```

---

## 🔄 Research Pipeline

The complete pipeline works as follows:

### Step 1 — Search

```python
search_agent.invoke(...)
```

The agent uses the Tavily-powered `web_search` tool to find relevant information.

### Step 2 — Read

```python
reader_agent.invoke(...)
```

The reader selects a useful URL and uses `scrape_url()` to extract webpage content.

### Step 3 — Write

```python
writer_chain.invoke(...)
```

The writer combines the search results and scraped content to create the final report.

### Step 4 — Critic

```python
critic_chain.invoke(...)
```

The critic evaluates the generated report and provides a score and feedback.

---

## 🎯 Why This Project?

Traditional research often requires:

1. Searching multiple websites
2. Reading many articles
3. Extracting useful information
4. Writing the report
5. Reviewing the report

This project automates that workflow using multiple specialized AI components.

Each component has a specific responsibility, making the overall system easier to understand and extend.

---

## 🔮 Future Improvements

Possible future improvements include:

* [ ] Add a web interface
* [ ] Add FastAPI REST API
* [ ] Add streaming responses
* [ ] Support multiple LLM providers
* [ ] Improve source ranking
* [ ] Add citation verification
* [ ] Add PDF report generation
* [ ] Add persistent research history
* [ ] Add database integration
* [ ] Add automated testing
* [ ] Add Docker support
* [ ] Improve error handling
* [ ] Add asynchronous execution
* [ ] Add more specialized research agents

---

## 📌 Current Limitations

* Web scraping depends on website accessibility.
* Some websites may block automated requests.
* Research quality depends on the retrieved sources and LLM output.
* API keys are required for external services.
* The current application is primarily command-line based.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add your feature"
```

5. Push the branch

```bash
git push origin feature/your-feature
```

6. Open a Pull Request

---

## 📄 License

This project is currently provided for educational and development purposes.

A formal open-source license can be added in the future.

---

## 👨‍💻 Author

**Rutik Kanzariya**

GitHub: [RutikKanzariya](https://github.com/RutikKanzariya)

Project: [Agent Research](https://github.com/RutikKanzariya/Agent_Research)

---

## ⭐ Acknowledgements

This project uses several open-source technologies and services:

* LangChain
* Groq
* Tavily
* BeautifulSoup
* Python

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Repository:** https://github.com/RutikKanzariya/Agent_Research
