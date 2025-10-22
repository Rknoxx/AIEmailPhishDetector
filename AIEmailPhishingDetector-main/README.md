## 🧠 AI Email Phishing Detector 🔒

A phishing detection system powered by artificial intelligence (AI) that uses machine learning and natural language processing (NLP) to distinguish between fake and real emails.This project, developed with Python, scikit-learn, pandas, and Streamlit, demonstrates how machine learning (ML) may improve email security by intelligently automating operations.

## 🚀 Features
- Converts text to TF-IDF vectors for numerical representation. 
- Cleans and preprocesses raw email content to remove URLs, special characters, and unnecessary symbols. 
- Evaluates Logistic Regression performance (precision, recall, F1-score) 
- Saves trained model and vectorizer for Joblib deployment 
- Works with Streamlit web app for real-time phishing detection.

## ⚙️ Installation & Setup

1. Clone the repository
git clone https://github.com/Rknoxx/AIEmailPhishDetector.git
cd AIEmailPhishDetector

2. Create virtual environment (PowerShell)
python -m venv .venv.\.venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Train the model
cd backend
python train.py

📄 Refer to How to run the project.txt for additional details.

## 🧩 How It Works

1)Preprocesses and cleans email data
2)Trains the ML model on TF-IDF features
3)Evaluates results and prints a classification report
4)Saves both model and vectorizer to /models
5)Streamlit app provides live phishing detection

## 🧭 Future Improvements

1)Integrate deep learning models (LSTM / BERT) for advanced NLP
2)Deploy a full-featured Streamlit web app
3)Build a browser/email plugin for real-time phishing detection
4)Use larger datasets (e.g., Enron, Kaggle Phishing Dataset)

##💻 Tech Stack

-Python -pandas / scikit-learn -TfidfVectorizer -Logistic Regression -Joblib -Streamlit

##📜 License

This project is licensed under the MIT License.

##👨‍💻 Author

Raj Patil
Master’s in Information Technology (Cybersecurity focus) @ Arizona State University
Interested in SOC Analyst, Threat Hunter, Cloud Security Engineer, and GRC roles
LinkedIn: https://www.linkedin.com/in/raj-patil834/  
