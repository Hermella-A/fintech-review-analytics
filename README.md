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

## Next Steps (Task 3 & 4)
- Store enriched data in **PostgreSQL** (database design, insertion).
- Create **final visualisations** and write a Medium‑style report with actionable recommendations for each bank.

## Branches
- `main` – stable, completed work (Tasks 1 & 2 merged).
- `task-1` – scraping and preprocessing.
- `task-2` – sentiment and thematic analysis.
- (future) `task-3` – PostgreSQL integration.
- (future) `task-4` – final report and dashboards.