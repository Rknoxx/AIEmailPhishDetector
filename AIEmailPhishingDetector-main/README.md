## 🧠 AI Email Phishing Detector 🔒
An AI-powered phishing email detector that uses Natural Language Processing (NLP) and Machine Learning to identify malicious vs. safe emails in real time.
Built with Python, scikit-learn, pandas, FastAPI, and Streamlit, this project demonstrates how ML can strengthen cybersecurity by automating phishing detection.

## 🚀 Features
•Cleans and preprocesses raw email text — removes URLs, symbols, and special characters
•Converts email text into TF-IDF vectors for numerical representation
•Trains a Logistic Regression model using a 10,000-record dataset (balanced phishing & safe emails)
•Evaluates using precision, recall, F1-score, and accuracy metrics
•Serves predictions via FastAPI backend (`/predict`)
•Interactive Streamlit frontend for real-time phishing detection
•Saves trained model and vectorizer for deployment using Joblib

## ⚙️ Installation & Setup
1.Clone the repository
git clone https://github.com/Rknoxx/AIEmailPhishDetector.git
cd AIEmailPhishDetector-main

2.Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   

3.Install dependencies
pip install -r requirements.txt

4.Train the model
cd backend
python train.py

5.Start backend server
uvicorn app:app --reload --port 8000

6.Start frontend Streamlit app
cd ../frontend
streamlit run streamlit_app.py

7. Refer to "How to run the program.txt" for fast deployment

## 🧩 How It Works
1.Data Preprocessing: cleans email text, removes noise, and tokenizes.
2.Feature Extraction: converts text into TF-IDF feature vectors.
3.Model Training: trains Logistic Regression classifier on 10K synthetic emails.
4.Evaluation: evaluates accuracy, precision, recall, and F1-score.
5.Serving: exposes `/predict` endpoint via FastAPI backend.
6.Frontend: Streamlit UI allows users to paste emails and analyze phishing probability.

## 📊 Model Evaluation (10K Dataset)

| Metric           | Value                                    |
| :--------------- | :--------------------------------------- |
| Precision    | ✅ 100%                                     |
| Recall       | ✅ 100%                                     |
| F1-Score     | ✅ 100%                                     |
| Accuracy     | ✅ 100%                                     |
| Dataset Size | 10,000 emails (5,000 phishing, 5,000 safe) |

> Prototype trained on synthetic dataset. Real-world data will likely yield ~93–96% precision once trained on Enron/Kaggle datasets.

## 🧠 Tech Stack
•Language: Python
•Libraries: pandas, scikit-learn, joblib, FastAPI, Streamlit
•Vectorization: TF-IDF (n-gram: 1–2)
•Model: Logistic Regression
•Dataset: 10K synthetic phishing & safe emails

## 🔮 Future Scope
 🧩 Integrate deep learning models (LSTM / BERT) for better NLP performance
 🌐 Deploy live via Streamlit Cloud / Docker
 🔒 Develop a browser/email plugin for real-time phishing alerts
 📈 Train on real-world datasets (Kaggle Phishing / Enron Email Corpora)
 🧰 Implement a metrics dashboard showing precision, recall, accuracy trends

## 🧪 Example Input (for testing)
Subject: Action Required: Verify Your Account
From: IT Support <no-reply@verify-account.example>

Dear User,
We detected unusual activity on your account and have temporarily limited access.
Please verify your account immediately: <PHISHING_URL>

If you do not act within 24 hours, your account may be suspended.

Regards,
IT Support
<DO_NOT_INCLUDE_CREDENTIAL_REQUEST>

Predicted Output:
> ⚠️ Warning: This looks like a phishing email!
> ML Probability: 98.7%

## 📜 License
This project is licensed under the MIT License.

## 👨‍💻 Author

Raj Patil
Master’s in Information Technology (Cybersecurity focus) at Arizona State University.
Interested in SOC Analyst, Threat Hunter, Cloud Security Engineer, and GRC roles.
🔗 LinkedIn: https://www.linkedin.com/in/raj-patil834
⭐ If you found this project useful, consider giving it a star on GitHub!


