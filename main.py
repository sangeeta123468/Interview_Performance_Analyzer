import pandas as pd
from sklearn.linear_model import LinearRegression

# Load dataset
def load_data():
    df = pd.read_csv("data.csv")
    return df

# Score calculation (with time)
def calculate_score(dsa, comm, prob, ques, time):
    return (dsa*0.4 + comm*0.2 + prob*0.3 + ques*0.1 - time*0.01)

# Suggestion logic
def get_suggestion(dsa, comm, prob):
    if dsa < 6:
        return "Improve DSA practice"
    elif comm < 6:
        return "Work on communication skills"
    elif prob < 6:
        return "Improve problem solving"
    else:
        return "Good performance"

# Process dataset
def process_data(df):
    df['Score'] = df.apply(lambda row: calculate_score(
        row['DSA'], row['Communication'], row['ProblemSolving'],
        row['QuestionsSolved'], row['TimeTaken']
    ), axis=1)
    return df

# Train ML model
def train_model(df):
    X = df[['DSA','Communication','ProblemSolving','QuestionsSolved','TimeTaken']]
    y = df['Score']

    model = LinearRegression()
    model.fit(X, y)

    return model