# Ask-Your-Data – AI-Powered Business Intelligence Assistant

Ask-Your-Data is a GenAI-powered business intelligence application that allows users to analyze structured business data using natural-language questions instead of manually writing SQL queries.

Users can explore sales data through an interactive dashboard or ask questions in plain English. The application uses Gemini to generate SQL queries, validates them, executes them against a MySQL database, and displays the results.

## Features

- Interactive business intelligence dashboard using real Superstore dataset records.
- Natural-language-to-SQL query generation using Gemini API.
- SQL validation to restrict queries to SELECT statements.
- MySQL database integration.
- Query result visualization and tabular data display.
- Business insights including sales, profit, orders, customers, categories, and regions.

## Technology Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Generative AI:** Google Gemini API
- **Database:** MySQL
- **Database Integration:** SQLAlchemy
- **SQL Validation:** SQLGlot
- **Data Analysis:** Pandas
- **Visualization:** Plotly

## How It Works

1. The user enters a business question in natural language.
2. Gemini generates an SQL query using the database schema.
3. SQLGlot validates the generated SQL query.
4. The validated query is executed against MySQL.
5. The application displays the query and its results.

## Dataset

This project uses the Sample Superstore dataset containing sales transactions and business information.

Dataset source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Download `Sample - Superstore.csv` and place it inside `data/raw/`.

The dataset is not included in this repository.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Bhumibahurupi23/ask-your-data.git
   cd ask-your-data
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Configure your `.env` file with your Gemini API key and MySQL connection credentials. Use the variable names expected by `schema_inspector.py`.

5. Create the MySQL database and tables using the project schema.

6. Download the dataset and place it in `data/raw/`.

7. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

## Security

- API keys and database credentials are stored in environment variables.
- `.env` and local dataset files are excluded through `.gitignore`.
- Generated SQL is validated before execution.

## Project Status

Developed as a portfolio project to explore Generative AI, natural-language database querying, SQL validation, and interactive business intelligence.
