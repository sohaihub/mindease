import streamlit as st
import gspread
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials
import json

# Page config
st.set_page_config(page_title="📚 MCQ Quiz", layout="wide", initial_sidebar_state="expanded")
st.title("📚 MCQ Question Bank")

# Google Sheets authentication
try:
    creds_json = {
  "type": "service_account",
  "project_id": "gen-lang-client-0825677129",
  "private_key_id": "863c182d09b2993ed46b34d5d2b0386e9366d750",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/Zm47l7r748wM\n95zvVtpxUiL/XqstrIZukWaUzOXVWjCOEHmxoQGQffmtdOo/ax6GVE0oFcI/P2U/\nfZkWTgXN55NfZjIAKT0irilKoDsQGirCP7F3ljFILFpfDQ+Drdk2mdI1ZazuNqsS\nNY8ionQziQ0q4cqNOqkwG0sl0Q4J8Qy42tDqPSIotJFy4v9J4yXjo9tn6eQqsxln\n7KakYJE6mO0fnPkP9QrsPaWW4DWTOqNG/bEWed89FNA6pJSbHENk5SCj8b4OdACY\nV2ClIiNhN/bx0rOE1z2L7goFPV5qcrXD9zfr56h2H7elhfAVqDGK/zYfFhcp0WjB\nD4u6RD5TAgMBAAECggEALSh3MKM7cCvOXG7dfZCx6FO3QyYsYBHZA+RVXh07ystF\nMneLps+0hUlbq8OucvkMkif4rlD37CFCe6jgAiW1c9/D4xnDCUuxi2mo/1zvonxy\nAzOw5OSwSvV/+vYjZ2+QlLPVJ1kOZIPMd/bgBw1qOjCHRUtRlWG2Qk3mPI1m8Qwg\nBaS1m0EgPymacp7oxt0XatBV0v7AUZPoe20YvnT2uY3eaJ/y9PiEQ2OyKoBiAdgp\nPRaX0tpVrXEGGuvaxfeV00bay+/A+kAE9Rr50GWs9OiR76h5UWU3T0xjXoL/2YyX\nlXCAPGwhSWVEjkNsAxlJ3UsjQxlTgJoCttP7H9pZdQKBgQDzdQpDrig1kmSjTAMT\nGyDrsyMWx9uboA73ncMT5WhMDcjiwTHtJeKVjW5IesIQ1lDEPREFB2l4wpLvfCLR\nBRMRGweEhGV3he52EMK8x6BzWljf6Cb2myx3Bd1xXkeFq2aimOTZn9lsTmvRFsvm\nNrf/qF7sSDV9b+YPmkmkxl0B7wKBgQDJQs8mCEYJvwBkfeNZ9lIjJRM2qKOQtnpo\nz2jOh4tm6o/A4mGuwyYhsmtfKNciRoz04WoP08pRRhZNptLtb04ZMy5DGIb8u+l+\n43fzFrVYZt8913lXYDeS++qwKeOJrnE5AcM+UfGMRSFlT6gDOSPAXc3Zoln0pU6B\nm/I7bNad3QKBgQCnda8cxLOFve+ZX1SSFMv9NFgDeG93SY5iBlND4T1vat/uEUOd\nQrzrb8AW/NF2MWSWxwZo9iM3XGcjcbilG5902am/Hi6JG0feUEMTBSE5l0Cgqxf5\n8tyP9inOrDH4IODVIOPxSYGNfReuV8bi0GqZ4R+B2V1prcmKm+7h90vMYwKBgQC4\neaN0QesorclHU1icMjqRej9FP4hFce17unlfrUAqwl+nthlBXiDKjEb8v2uKQE6d\neyyDe2ab3nk9DeeSuQ5F7PK/j3DToc5hf1CIIc1xTUHc5m+Tll76PCye8pZcseeY\nEDSNIAEeyJLW0Q+4fJx3i8POc5CuvQLbrDx5GccShQKBgGBnCUgdD/pzH1qsVBNo\nGc/Dxrx5A1jpluWgq+O7+dSNScczNjII4rM8H/e5yfC1/e2gK/HA3LeIwxYWuCBT\nFpI9/ZpOC5DIawkPsm5ac9FUT+b5uXnuyEK+mecPrt1imRuhm/VL4EdhVlHnsTHy\nrdSdFMJoZKOJrPeOPSKiR5Mb\n-----END PRIVATE KEY-----\n",
  "client_email": "data-774@gen-lang-client-0825677129.iam.gserviceaccount.com",
  "client_id": "101552404875723380663",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-774%40gen-lang-client-0825677129.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

    client = gspread.service_account_from_dict(creds_json)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1K2HJSL0U0vay4UaW4s3QPAIkQ_noj742ZRQJxbTTbQ0")
    worksheet = spreadsheet.get_worksheet(0)
    raw_records = worksheet.get_all_records()
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.stop()

# Page selection
page = st.sidebar.selectbox("📑 Select a Page", ["Topic Stats", "Questions"])

# Difficulty map for sorting
diff_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}

if page == "Topic Stats":
    st.subheader("📊 Overview")
    total = len(raw_records)
    st.markdown(f"### ✅ Total Questions: {total}")

    topic_count = {}
    difficulty_count = {}

    for row in raw_records:
        topic = row.get("Topic", "Unknown").strip().title()
        diff = row.get("Difficulty", "Unknown").strip().title()

        topic_count[topic] = topic_count.get(topic, 0) + 1
        difficulty_count[diff] = difficulty_count.get(diff, 0) + 1

    # 👉 Total Topics
    st.markdown(f"### 🧠 Total Topics: {len(topic_count)}")

    # 📋 Topic-wise Question Count Table
    topic_table = [{"Topic": t, "No. of Questions": c} for t, c in sorted(topic_count.items(), key=lambda x: x[1], reverse=True)]
    st.markdown("### 📋 Topic-wise Question Count")
    st.table(topic_table)

    # 🥧 Top 10 Topics Pie Chart
    top_topics = dict(sorted(topic_count.items(), key=lambda x: x[1], reverse=True)[:10])
    fig1 = px.pie(names=list(top_topics.keys()), values=list(top_topics.values()), title="Top 10 Topics")
    st.plotly_chart(fig1, use_container_width=True)

    # 📊 Difficulty Distribution Bar Chart
    fig2 = px.bar(
        x=list(difficulty_count.keys()),
        y=list(difficulty_count.values()),
        labels={'x': 'Difficulty', 'y': 'Questions'},
        title='Difficulty Distribution',
        color=list(difficulty_count.values()),
        color_continuous_scale='Blues'
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Questions":
    topics = sorted(set(row.get("Topic", "Unknown").strip().title() for row in raw_records))
    selected_topic = st.sidebar.selectbox("📌 Select Topic", topics)

    filtered = [r for r in raw_records if r.get("Topic", "").strip().title() == selected_topic]
    diff_levels = sorted(set(r.get("Difficulty", "Unknown").strip().title() for r in filtered))
    selected_diff = st.sidebar.selectbox("🎚️ Select Difficulty", ["All"] + diff_levels)

    if selected_diff != "All":
        filtered = [r for r in filtered if r.get("Difficulty", "").strip().title() == selected_diff]

    for idx, row in enumerate(filtered, 1):
        st.markdown(f"### Question {idx}")
        st.write(row.get("Question", "N/A"))

        options = row.get("Options", "").split(";")
        for opt in options:
            st.markdown(f"- {opt.strip()}")

        correct = row.get("Correct Answer", "").strip().upper()
        opt_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        if correct in opt_map and opt_map[correct] < len(options):
            st.success(f"✅ Answer: {options[opt_map[correct]].strip()}")
        else:
            st.error("❌ Invalid Answer")

        st.markdown("---")
