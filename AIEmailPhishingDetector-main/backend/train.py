import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib, os, re, sys

# Paths (adjust if your file location is different)
DATA_PATH = os.path.join("..", "data", "emails.csv")
MODEL_DIR = os.path.join("..", "models")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)  # replace URLs
    text = re.sub(r"[^a-z0-9\s]", " ", text)          # remove punctuation
    text = re.sub(r"\s+", " ", text)                  # collapse multiple spaces
    return text.strip()

# --- Read CSV robustly (handles headerless files like your sample) ---
if not os.path.exists(DATA_PATH):
    sys.exit(f"❌ Data file not found at {DATA_PATH}. Check the path.")

# Peek first few rows to guess if header exists
try:
    preview = pd.read_csv(DATA_PATH, nrows=5)
except Exception as e:
    # If normal read fails (e.g., because of no header quoting issues), try headerless read directly
    preview = pd.read_csv(DATA_PATH, header=None, nrows=5, quotechar='"', skipinitialspace=True)

# Decide reading strategy
use_header = False
cols = [str(c).lower() for c in preview.columns.tolist()]

if any(c in ("text", "email", "message", "content") for c in cols) and any(c in ("label", "category", "target", "class") for c in cols):
    use_header = True

if use_header:
    df = pd.read_csv(DATA_PATH)
else:
    # Your sample is headerless with two columns: text and label
    df = pd.read_csv(DATA_PATH, header=None, names=["text", "label"], quotechar='"', skipinitialspace=True)

# Debug output
print("📌 Columns after reading:", df.columns.tolist())
print(df.head(8))

# Validate we have the expected columns
if "text" not in df.columns or "label" not in df.columns:
    sys.exit("❌ Could not locate 'text' and 'label' columns after reading the CSV. Please check the file format.")

# Ensure label is numeric (0/1). Convert if necessary.
try:
    df["label"] = df["label"].astype(int)
except Exception:
    # try to map common label strings to numeric
    mapping = {"phishing": 1, "spam": 1, "ham": 0, "safe": 0, "legit": 0}
    df["label"] = df["label"].astype(str).str.lower().map(mapping)
    if df["label"].isnull().any():
        # if mapping failed for some rows, attempt simple numeric conversion with errors='coerce'
        df["label"] = pd.to_numeric(df["label"], errors="coerce")
    if df["label"].isnull().any():
        print("⚠️ Some labels could not be converted to integers. Here are problem rows:")
        print(df[df["label"].isnull()])
        sys.exit("❌ Fix label values in the CSV (should be 0/1 or known strings like 'phishing','ham').")

# Clean text column and continue
df["text_clean"] = df["text"].astype(str).apply(clean_text)

X = df["text_clean"]
y = df["label"]

# Vectorize
vec = TfidfVectorizer(max_features=5000)
X_vec = vec.fit_transform(X)

# Train model
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
print("\n📊 Classification Report:")
print(classification_report(y_test, model.predict(X_test)))

# Save
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(vec, os.path.join(MODEL_DIR, "vectorizer.joblib"))
joblib.dump(model, os.path.join(MODEL_DIR, "clf.joblib"))
print(f"✅ Model and vectorizer saved to '{MODEL_DIR}/'")
