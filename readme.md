# AI Medical Assistant

A web-based educational project using FastAPI, MySQL,
HTML/CSS/JavaScript, and an AI wellness chatbot powered by Ollama with
Llama 3.2.

> **Medical safety:** This is an educational prototype. AI responses can
> be inaccurate and must not be treated as a diagnosis or prescription.

## Features

-   User registration and login
-   AI wellness chatbot and chat history
-   Daily diet and routine tracking
-   Doctor and appointment functionality where implemented in the
    current version

## Prerequisites

Install Python, MySQL Server, and (for chatbot features) Ollama. Git and
a modern browser are also useful.

## 1. Get the project

``` bash
git clone https://github.com/kulveerchand/medical-assistant-backend.git
cd medical-assistant-backend
```

If you already have the project, open a terminal in the folder
containing `app/` and `requirements.txt`.

## 2. Create a Python environment (Windows)

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt and run
`venv\Scripts\activate.bat`.

## 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If there is no `requirements.txt`, check the project's imports and
install its dependencies. Typical packages include:

``` powershell
pip install fastapi "uvicorn[standard]" sqlalchemy pymysql python-dotenv ollama
```

## 4. Configure MySQL

1.  Start MySQL Server.
2.  Create a database (example):

``` sql
CREATE DATABASE medical_assistant;
```

3.  Create a `.env` file in the project root with the database variables
    used by `app/database.py`:

``` dotenv
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=medical_assistant
```

Replace the example credentials with your own and ensure `DB_NAME`
matches the database you created. Never commit `.env` or share its
secrets. Tables may be created automatically if the current application
enables SQLAlchemy `Base.metadata.create_all(...)`.

## 5. Set up Ollama (chatbot only)

Install Ollama, then run:

``` powershell
ollama pull llama3.2
ollama list
```

Keep Ollama running while testing AI chat. The project has used the
local Ollama service at `http://127.0.0.1:11434`; make sure the
configured model name matches the downloaded model.

## 6. Start the backend

From the backend project root:

``` powershell
python -m uvicorn app.main:app --reload
```

Keep the terminal open. Open these URLs in your browser:

-   API root: http://127.0.0.1:8000/
-   Swagger UI: http://127.0.0.1:8000/docs
-   ReDoc: http://127.0.0.1:8000/redoc
-   OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Stop the server with `Ctrl+C`.

### If it fails to start

-   Run the command from the project root, not from inside `app/`.
-   Confirm `app/main.py` exists and dependencies are installed in the
    active environment.
-   Check that MySQL is running and `.env` values are correct.
-   If `Could not import module "app.main"` appears, verify the folder
    structure and working directory.

## 7. Open the frontend

Locate the frontend HTML file in your project (for example, `login.html`
or `index.html`). You can open it with VS Code Live Server, or start a
simple server from the frontend folder in a second terminal:

``` powershell
python -m http.server 5500
```

Open http://127.0.0.1:5500 and navigate to the correct HTML page. Check
that the frontend JavaScript points to the backend:

``` javascript
const API_URL = "http://127.0.0.1:8000";
```

Keep the backend running. If browser requests fail, check the browser
console, backend terminal, API URL, and FastAPI CORS settings for the
frontend origin.

## 8. Test the project

1.  Visit http://127.0.0.1:8000/docs.
2.  Expand an endpoint, select **Try it out**, enter the required
    fields, and click **Execute**.
3.  Test the endpoints that exist in your current version:
    registration/login, chat, chat history, diet, and routine.
4.  Check MySQL to confirm records save and retrieve correctly.
5.  Test the frontend and inspect browser-console errors.

Report a feature as working only after testing it in your environment.

## Common problems

  --------------------------------------------------------------------------
  Problem                                What to check
  -------------------------------------- -----------------------------------
  MySQL connection error                 MySQL service, credentials,
                                         database name, port, and `.env`

  `ModuleNotFoundError`                  Activate the correct environment
                                         and install dependencies

  `Could not import module "app.main"`   Run Uvicorn from the project root;
                                         verify `app/main.py`

  AI chatbot fails                       Ollama is running, `llama3.2` is
                                         installed, and model names match

  Frontend cannot reach API              Backend status, `API_URL`, and CORS
                                         configuration

  Port 8000 is occupied                  Stop the process using it or select
                                         another port and update `API_URL`
  --------------------------------------------------------------------------

## Security

-   Do not commit `.env`, passwords, tokens, or other secrets.
-   `--reload` is for local development, not production.
-   Protect private records with server-side authentication and
    authorization.
-   Do not use real patient data in demos or public repositories.

## Example backend structure

``` text
medical-assistant-backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   └── routes/
├── requirements.txt
├── .env          # create locally; do not commit
├── .gitignore
└── README.md
```

## Maintainer

**Kulveer Chand**\
B.Tech --- Computer Science and Engineering (AI & Data Science)\
Sangam University, Bhilwara, Rajasthan
