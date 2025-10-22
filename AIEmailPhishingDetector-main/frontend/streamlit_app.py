import streamlit as st
import requests
import re
import os
import base64

BACKEND_URL = "http://127.0.0.1:8000/predict"

# ================== Load Custom CSS ==================
def load_css(file_name="styles.css"):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS
load_css()

# ================== Background Image ==================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "assets/cyber_banner.png"
if os.path.exists(img_path):
    img_base64 = get_base64_of_bin_file(img_path)
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ================== Validation Function ==================
def is_valid_email_text(text: str) -> bool:
    text = text.strip()
    if re.match(r"^[\d\s]", text):
        return False
    if len(text.split()) < 5:
        return False
    if re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
        return False
    return True

# ================== Title ==================
st.title("📧 AI Email Phishing Detector")

# ================== Input Area ==================
email_text = st.text_area("Paste email content here:")

# ================== Analyze Button ==================
if st.button("Analyze"):
    if not email_text.strip():
        st.error("Please provide email content for analysis.")
    elif not is_valid_email_text(email_text):
        st.error("Invalid Email")
    else:
        try:
            response = requests.post(BACKEND_URL, json={"text": email_text})
            if response.status_code == 200:
                data = response.json()

                st.markdown("### 📊 Results")
                st.write("**ML Probability:**", f"{data['phishing_probability']:.2%}")
                st.write("**Heuristic Score:**", f"{data['heuristic_score']:.2%}")
                st.write("**Final Probability:**", f"{data['final_prob']:.2%}")

                # ================== Main Result ==================
                if data["label"] == 1:
                    st.markdown(
                        """
                        <div class="stAlert error">
                            🚨 Warning: This looks like a phishing email!
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div class="stAlert success">
                            ✅ This looks safe.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # ---- NEW FUNCTIONALITIES ----
                # Risk Score Gauge
                st.subheader("📈 Risk Score")
                st.metric("Final Probability", f"{data['final_prob']:.0%}")
                st.progress(data["final_prob"])

                # Suspicious Elements Breakdown (User-Friendly Labels)
                st.subheader("🔎 Suspicious Elements")

                friendly_labels = {
                    "ml_model": "AI Content Risk",
                    "url_features": "Link Risk",
                    "phrases": "Urgency Risk"
                }

                for k, v in data.get("suspicious_breakdown", {}).items():
                    label = friendly_labels.get(k, k)
                    st.write(f"**{label}**: {v:.0%}")
                    st.progress(v)

                # Link Preview
                st.subheader("🔗 Link Preview")
                if data.get("link_preview"):
                    lp = data["link_preview"]

                    if lp["mismatch"]:
                        st.markdown(
                            """
                            <div class="stAlert error">
                                ⚠️ Suspicious domain detected!
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.write(f"🔗 {lp['url']}")
                    else:
                        st.markdown(
                            """
                            <div class="stAlert success">
                                ✅ Domain looks safe
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.write(f"🔗 {lp['url']}")
                else:
                    st.write("No links found")

                # Export Report
                st.subheader("📑 Report")
                st.download_button(
                    "Save Report",
                    str(data),
                    file_name="phishing_report.txt"
                )

            else:
                st.error("❌ Error connecting to backend API.")

        except Exception as e:
            st.error(f"⚠️ Exception: {e}")
