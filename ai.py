import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# Extract text from PDF
# =========================
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text.lower()


# =========================
# Clean Text
# =========================
def clean_text(text):
    text = re.sub(r'\W+', ' ', text)  # remove special characters
    return text.lower()


# =========================
# Calculate ATS Score
# =========================
def calculate_similarity(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words='english',      # remove common words
        ngram_range=(1, 2),        # consider single + double words
    )

    tfidf = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

    score = float(similarity[0][0]) * 100

    return round(score, 2)


# =========================
# Keyword Analysis
# =========================
def keyword_analysis(resume_text, job_description):
    resume_words = set(clean_text(resume_text).split())
    jd_words = set(clean_text(job_description).split())

    matched = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    # Remove very small words
    matched = [w for w in matched if len(w) > 2]
    missing = [w for w in missing if len(w) > 2]

    return matched[:15], missing[:15]