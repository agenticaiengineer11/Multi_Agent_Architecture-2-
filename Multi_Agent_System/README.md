# Meta-Agent Factory

The project includes a professional Streamlit workspace for running the
LangGraph multi-agent system. The interface supports task prompts, PDF context
uploads, execution telemetry, response history, and generated coding results.

## Run locally

```powershell
cd Multi_Agent_System
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file with the credentials required by the selected agents:

```text
GROQ_API_KEY=your-groq-key
TAVILY_API_KEY=your-tavily-key
```

## Deploy with Docker

```powershell
docker compose up --build
```

Then open `http://localhost:8501`. The included `Dockerfile` listens on
`0.0.0.0:8501`, which is compatible with container platforms such as Render,
Railway, Fly.io, and Google Cloud Run. `render.yaml` provides a ready-to-use
Render service definition; add the two API keys as platform secrets.

## CLI mode

The original command-line entry point remains available:

```powershell
python main.py
```