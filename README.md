# Fintech Review Analytics – Customer Experience for Ethiopian Bank Apps

## Project Overview
This project analyzes Google Play Store reviews for three Ethiopian banks:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

The goal is to extract actionable insights about user satisfaction, pain points, and feature requests using web scraping, sentiment analysis, and thematic extraction.

## Repository Structure
├── .github/workflows/ # CI/CD pipeline
├── data/raw/ # CSV files (ignored by Git)
├── notebooks/ # Jupyter notebooks for each task
├── src/ # Source code (future)
├── tests/ # Unit tests
├── scripts/ # Utility scripts
├── .gitignore
├── requirements.txt
└── README.md


## Setup Instructions
1. Clone the repository  
   `git clone https://github.com/Hermella-A/fintech-review-analytics.git`
2. Create a virtual environment  
   `python -m venv venv`
3. Activate it  
   `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies  
   `pip install -r requirements.txt`
5. Download spaCy model (for Task 2)  
   `python -m spacy download en_core_web_sm`

## Completed Tasks

### Task 1 – Data Collection and Preprocessing
- **Notebook:** `scrape_reviews.ipynb`
- Scraped 500+ reviews per bank using `google-play-scraper` (total 1500 reviews).
- Performed cleaning: removed duplicates, handled missing values, normalised dates.
- Saved cleaned dataset as `cleaned_reviews.csv` (not committed to Git).
- **Key result:** Clean, analysis-ready dataset with columns: `review`, `rating`, `date`, `bank`, `source`.

### Task 2 – Sentiment and Thematic Analysis
- **Notebook:** `sentiment_analysis.ipynb`
- Applied **TextBlob** to classify each review as POSITIVE, NEGATIVE, or NEUTRAL.
- Aggregated sentiment per bank and per star rating.
- Extracted top keywords per bank using TF‑IDF.
- Grouped keywords into business-relevant themes (e.g., Performance, Authentication, Features).
- Generated visualisations: sentiment distribution (stacked bar chart), average sentiment by rating (bar chart), theme frequency per bank.
- Saved enriched dataset as `reviews_with_sentiment.csv`.

## Task 3 – PostgreSQL Database

### Schema Design
- **Database name:** `bank_reviews`
- **Tables:**
  - `banks`: bank_id (PK), bank_name, app_name
  - `reviews`: review_id (PK), bank_id (FK), review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source

The SQL schema is available in `sql/schema.sql`.

### Data Insertion
The Python script `src/populate_db.py` uses `psycopg2` and `sqlalchemy` to:
- Create the database (if not exists)
- Create the tables
- Insert cleaned and enriched review data

Total reviews inserted: **1134**

### Verification Results
- **Reviews per bank:**
  - Commercial Bank of Ethiopia: 376
  - Dashen Bank: 380
  - Bank of Abyssinia: 378
- **Average rating per bank:**
  - Commercial Bank of Ethiopia: 3.92
  - Dashen Bank: 3.94
  - Bank of Abyssinia: 3.23
- **Missing data:** 0 rows with null review text or rating.

All integrity checks passed.

### Setup Instructions (for running the script)
1. Install PostgreSQL locally.
2. Create a database `bank_reviews` (the script can create it).
3. Update the database connection parameters in `src/populate_db.py` (user, password, host, port).
4. Run `python src/populate_db.py`.
5. Verify with `python src/verify_db.py` or a notebook cell.

## Task 4 – Insights and Recommendations

### Key Findings
- **Bank of Abyssinia (BOA)** has the lowest average rating (3.23) and highest proportion of negative reviews. The keyword "worst" appears frequently.
- **Commercial Bank of Ethiopia (CBE)** and **Dashen Bank** have higher ratings (~3.9) and positive keywords ("good", "nice", "best").

### Visualizations
- Sentiment distribution stacked bar chart  
- Rating distribution boxplots per bank  
- Top 10 keywords per bank (horizontal bar charts)

### Recommendations
- **CBE:** Improve update stability; add fingerprint login.
- **BOA:** Fix critical crashes; improve OTP reliability.
- **Dashen:** Unify branding (remove "amole"); optimise transaction speed.

### Deliverable
- Final report (Medium blog style, PDF) with up to 10 pages and 10 plots.
- Notebook `insights_recommendations.ipynb` containing all final visualizations and analysis.

## Branches
- `main` – stable, completed work (Tasks 1 & 2 merged).
- `task-1` – scraping and preprocessing.
- `task-2` – sentiment and thematic analysis.
- `task-3` – PostgreSQL integration.
-  `task-4` – final report and dashboards.