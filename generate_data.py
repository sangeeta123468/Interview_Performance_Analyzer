import pandas as pd
import random

# Real Indian names list
names = [
    "Sangeeta","Aman","Riya","Rahul","Neha","Karan","Simran","Arjun","Priya","Ankit",
    "Pooja","Rohit","Sneha","Vikas","Nisha","Deepak","Kriti","Aditya","Meena","Saurav",
    "Anjali","Shivam","Aarti","Manish","Kavita","Sunil","Preeti","Ramesh","Divya","Anurag",
    "Sakshi","Gaurav","Payal","Abhishek","Komal","Tarun","Seema","Vivek","Rekha","Harsh",
    "Tanya","Nitin","Monika","Yash","Pankaj","Jyoti","Varun","Isha","Rajat","Muskan"
]

data = []

for i in range(1000):
    name = random.choice(names) + "_" + str(i)   # unique name

    dsa = random.randint(1,10)
    comm = random.randint(1,10)
    prob = random.randint(1,10)
    time = random.randint(15,70)
    ques = random.randint(1,6)

    data.append([name, dsa, comm, prob, time, ques])

df = pd.DataFrame(data, columns=[
    "Name","DSA","Communication","ProblemSolving","TimeTaken","QuestionsSolved"
])

df.to_csv("data.csv", index=False)

print("✅ 1000 REAL-NAME dataset generated!")