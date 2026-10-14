# Text-to-SQL with Python, Gemini, and SQLite

## Set up on Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

SQLite is included with Python, so it needs no separate installation. If PowerShell blocks virtual-environment activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Add your API key securely

1. Open Google AI Studio's API keys page: <https://aistudio.google.com/app/apikey>.
2. Create a secret key and copy it when shown. Treat it like a password; do not share it or commit it.
3. Open `.env` in this project and replace `your_api_key_here` with the key:

   ```dotenv
   GEMINI_API_KEY=your_secret_key
   GEMINI_MODEL=gemini-3.5-flash-lite
   ```

`.env` is excluded by `.gitignore`. Keep it local, and rotate the key in Google AI Studio if it is exposed. API usage may incur charges.

## Create the sample database and run

```powershell
python create_db.py
python text_to_sql.py
```

The console prints the schema at startup. Enter a question such as `Show the top customers by spending`; results appear in a table. Type `schema` to show the schema again, or `quit`/`exit` to close the console. The app asks the model for one SQLite `SELECT` query and executes it using a read-only connection. Generated SQL is checked before execution, and SQLite blocks write operations. Success and error messages use terminal colors.

The app uses Google's official `google-genai` Python SDK and Gemini Interactions API.
