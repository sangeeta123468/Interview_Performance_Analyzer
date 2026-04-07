import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import load_data, calculate_score, get_suggestion, process_data, train_model

st.title("🎯 Smart Interview Performance Analyzer")

# ---------------- FILE UPLOAD ----------------
st.header("📂 Upload Your Dataset")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# SAFE DATA LOADING 🔥
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
else:
    try:
        df = load_data()
    except:
        st.error("⚠️ data.csv not found! Please upload a file or generate dataset.")
        st.stop()

# ---------------- PROCESS + MODEL ----------------
df = process_data(df)
model = train_model(df)

# ---------------- PREVIEW ----------------
st.write("### 📊 Dataset Preview")
st.dataframe(df.head())

# ---------------- TOP PERFORMER ----------------
st.header("🏆 Top Performer")
top = df.sort_values(by="Score", ascending=False).iloc[0]
st.write(f"Name: {top['Name']}")
st.write(top)

# ---------------- LEADERBOARD ----------------
st.header("🏆 Leaderboard (Top 10)")
st.dataframe(df.sort_values(by="Score", ascending=False).head(10))

# ---------------- INPUT ----------------
st.header("Enter Candidate Performance")

name = st.text_input("Candidate Name")
dsa = st.number_input("DSA Score", 0, 10, 5)
comm = st.number_input("Communication Score", 0, 10, 5)
prob = st.number_input("Problem Solving Score", 0, 10, 5)
ques = st.number_input("Questions Solved", 0, 6, 3)
time = st.number_input("Time Taken (minutes)", 10, 120, 30)

# ---------------- SCORE ----------------
score = calculate_score(dsa, comm, prob, ques, time)
st.subheader(f"📊 Final Score: {round(score,2)}")

# ---------------- ML ----------------
predicted_score = model.predict([[dsa, comm, prob, ques, time]])
predicted_score = max(0, min(10, predicted_score[0]))
st.write(f"🤖 Predicted Score (ML): {round(predicted_score,2)}")

# ---------------- CATEGORY ----------------
if score >= 8:
    st.success("🌟 Excellent Performance")
elif score >= 6:
    st.info("👍 Good Performance")
else:
    st.warning("⚠️ Needs Improvement")

# ---------------- SUGGESTION ----------------
st.write("### Suggestion:", get_suggestion(dsa, comm, prob))

# ---------------- RADAR ----------------
labels = ['DSA','Communication','Problem Solving']
values = [dsa, comm, prob]

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

angles = [n / float(len(labels)) * 2 * 3.14 for n in range(len(labels))]
angles += angles[:1]
values += values[:1]

ax.plot(angles, values)
ax.fill(angles, values, alpha=0.3)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

st.pyplot(fig)

# ---------------- DISTRIBUTION ----------------
st.header("📊 Score Distribution")
fig1 = plt.figure()
plt.hist(df['Score'], bins=10)
st.pyplot(fig1)

# ---------------- SCATTER ----------------
st.header("📈 DSA vs Score")
fig2 = plt.figure()
plt.scatter(df['DSA'], df['Score'])
st.pyplot(fig2)

# ---------------- TOP 5 ----------------
st.header("🏆 Top 5 Candidates")
top5 = df.sort_values(by="Score", ascending=False).head(5)
fig3 = plt.figure()
plt.bar(range(len(top5)), top5['Score'])
st.pyplot(fig3)

# ---------------- HEATMAP (FIXED) ----------------
st.header("📊 Correlation Heatmap")
numeric_df = df.select_dtypes(include=['number'])

fig4 = plt.figure()
sns.heatmap(numeric_df.corr(), annot=True)

st.pyplot(fig4)

# ---------------- COMPARE ----------------
st.header("⚔️ Compare Two Candidates")

names = df['Name'].unique()

cand1 = st.selectbox("Select Candidate 1", names)

# Remove selected candidate from second list
remaining_names = [n for n in names if n != cand1]

cand2 = st.selectbox("Select Candidate 2", remaining_names)

data1 = df[df['Name'] == cand1].iloc[0]
data2 = df[df['Name'] == cand2].iloc[0]

comparison_df = pd.DataFrame({
    "Feature": ["DSA","Communication","ProblemSolving","Score"],
    cand1: [data1['DSA'], data1['Communication'], data1['ProblemSolving'], data1['Score']],
    cand2: [data2['DSA'], data2['Communication'], data2['ProblemSolving'], data2['Score']]
})

st.dataframe(comparison_df)

# -------- COMPARISON GRAPH --------
fig5 = plt.figure()

labels = ["DSA","Communication","ProblemSolving"]
values1 = [data1['DSA'], data1['Communication'], data1['ProblemSolving']]
values2 = [data2['DSA'], data2['Communication'], data2['ProblemSolving']]

x = range(len(labels))

plt.bar(x, values1, width=0.4, label=cand1)
plt.bar([i+0.4 for i in x], values2, width=0.4, label=cand2)

plt.xticks([i+0.2 for i in x], labels)
plt.legend()

st.pyplot(fig5)

# ---------------- DOWNLOAD ----------------
st.header("📥 Download Report")

result_df = pd.DataFrame({
    "Name":[name],
    "DSA":[dsa],
    "Communication":[comm],
    "ProblemSolving":[prob],
    "Time":[time],
    "Score":[score],
    "Predicted":[predicted_score]
})

st.download_button("Download CSV", result_df.to_csv(index=False), "report.csv")