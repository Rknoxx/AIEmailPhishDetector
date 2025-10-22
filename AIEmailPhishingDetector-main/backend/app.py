# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os, re
import numpy as np
from urllib.parse import urlparse

# ================== Load Model ==================
BASE_DIR = os.path.dirname(__file__)
VEC = joblib.load(os.path.join(BASE_DIR, "..", "models", "vectorizer.joblib"))
CLF = joblib.load(os.path.join(BASE_DIR, "..", "models", "clf.joblib"))

# ================== Cleaning ==================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.strip()

# ================== Heuristics ==================
URL_RE = re.compile(r"https?://[^\s'\"<>]+")
URGENCY_WORDS = {"urgent", "immediately", "verify", "action required", "click here"}

def extract_urls(text: str):
    return URL_RE.findall(text)

def url_heuristic(url: str):
    score, reasons = 0.0, []
    try:
        p = urlparse(url)
        host = p.hostname or ""
    except Exception:
        host = ""
    if len(url) > 80:
        reasons.append("Very long URL")
        score += 0.1
    if any(tld in host for tld in [".ru", ".cn", ".tk"]):
        reasons.append("Suspicious TLD")
        score += 0.2
    if "login" in url or "verify" in url:
        reasons.append("Phishing keyword in URL")
        score += 0.2
    return {"url": url, "score": score, "reasons": reasons}

def phrase_heuristic(text: str):
    score, matches = 0.0, []
    low = text.lower()
    for w in URGENCY_WORDS:
        if w in low:
            matches.append(w)
            score += 0.1
    return {"score": min(1.0, score), "matches": matches}

# ================== Explainability ==================
def top_tokens(text: str, top_k=5):
    X = VEC.transform([text])
    probs = CLF.predict_proba(X)[0]
    phishing_prob = float(probs[1])
    try:
        feat_names = VEC.get_feature_names_out()
        coefs = CLF.coef_[0]
        contribs = X.toarray()[0] * coefs
        idx = np.argsort(-contribs)[:top_k]
        tokens = [{"token": feat_names[i], "weight": float(contribs[i])}
                  for i in idx if contribs[i] > 0]
    except Exception:
        tokens = []
    return phishing_prob, tokens

# ================== API ==================
app = FastAPI()

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "ok", "message": "Phishing Detector API"}

@app.post("/predict")
def predict_email(req: EmailRequest):
    text = clean_text(req.text)

    # ML prediction
    ml_prob, tokens = top_tokens(text)

    # Heuristics
    urls = extract_urls(req.text)
    url_reports = [url_heuristic(u) for u in urls]
    phrase = phrase_heuristic(req.text)
    heuristic_score = max([u["score"] for u in url_reports], default=0) + phrase["score"]
    heuristic_score = min(1.0, heuristic_score)

    # Final probability (blend ML + heuristics)
    final_prob = 0.65 * ml_prob + 0.35 * heuristic_score
    label = int(final_prob >= 0.35)

    # Link preview
    preview = None
    if urls:
        first_url = urls[0]
        host = urlparse(first_url).hostname or ""
        preview = {
            "url": first_url,
            "mismatch": any(tld in host for tld in [".ru", ".cn", ".tk"])
        }

    # Suspicious breakdown
    suspicious_breakdown = {
        "ml_model": float(ml_prob),
        "url_features": float(max([u["score"] for u in url_reports], default=0)),
        "phrases": float(phrase["score"]),
    }

    return {
        "label": label,
        "phishing_probability": ml_prob,
        "heuristic_score": heuristic_score,
        "final_prob": final_prob,
        "explanations": {
            "top_tokens": tokens,
            "url_reports": url_reports,
            "phrase": phrase,
        },
        "link_preview": preview,
        "suspicious_breakdown": suspicious_breakdown
    }
