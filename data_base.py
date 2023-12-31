"""Calculate student grades by combining data from many sources.

Using Pandas, this script combines data from the:

* Roster
* Homework & Exam grades
* Quiz grades

to calculate final grades for a class.
"""
#Importing Libraries and Setting Paths
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

#Data Importation and Cleaning
roster = pd.read_csv(DATA_FOLDER / 'roster.csv', converters={'NetID': str.lower, 'Email Address': str.lower}, index_col='NetID')


hw_exam_grades = pd.read_csv(DATA_FOLDER / 'hw_exam_grades.csv', converters={'SID': str.lower}, usecols=lambda col: 'Submission' not in col, index_col='SID')


quiz_grades = pd.DataFrame()
for i in range(1, 6):  # Assuming there are 5 quizzes
    quiz_df = pd.read_csv(DATA_FOLDER / f'quiz_{i}_grades.csv', converters={'Email': str.lower})
    quiz_df.drop(columns=['Last Name', 'First Name'], inplace=True)  # Drop overlapping columns
    quiz_df.rename(columns={'Grade': f'Quiz {i}'}, inplace=True)
    quiz_df.set_index('Email', inplace=True)

    if quiz_grades.empty:
        quiz_grades = quiz_df
    else:
        quiz_grades = quiz_grades.join(quiz_df, how='outer')

# Fill missing values with 0
quiz_grades.fillna(0, inplace=True)

#Data Merging: roaster and homework
final_data = pd.merge(roster, hw_exam_grades, left_index=True, right_index=True)


#Data Merging: Final data and quiz grades
final_data = pd.merge(final_data, quiz_grades, left_on='Email Address', right_index=True)


final_data = final_data.fillna(0)

#Data Processing and Score Calculation
n_exams = 3
#For each exam, calculate the score as a proportion of the maximum points possible.
#Remove pass once you have cerated written the for loop
for n in range(1, n_exams + 1):
    exam_score_col = f'Exam {n}'
    exam_max_col = f'Exam {n} - Max Points'
    final_data[exam_score_col] = final_data[exam_score_col] / final_data[exam_max_col]


#Calculating Exam Scores:
#Filter homework and Homework - for max points
homework_scores = final_data.filter(regex='^Homework \d+$')
homework_max_points = final_data.filter(regex='^Homework \d+ - Max Points$')

#Calculating Total Homework score
sum_of_hw_scores = homework_scores.sum(axis=1)
sum_of_hw_max = homework_max_points.sum(axis=1)
final_data["Total Homework"] = sum_of_hw_scores / sum_of_hw_max

#Calculating Average Homework Scores
hw_max_renamed = homework_max_points.rename(columns=lambda x: x.replace(' - Max Points', ''))
average_hw_scores = (homework_scores / hw_max_renamed).sum(axis=1) / len(hw_max_renamed.columns)
final_data["Average Homework"] = average_hw_scores

#Final Homework Score Calculation
final_data["Homework Score"] = final_data[["Total Homework", "Average Homework"]].max(axis=1)

#Calculating Total and Average Quiz Scores:
#Filter the data for Quiz scores
quiz_scores = final_data.filter(regex='^Quiz \d+$')

quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)

#Final Quiz Score Calculation:
sum_of_quiz_scores = quiz_scores.sum(axis=1)
sum_of_quiz_max = quiz_max_points.sum()
final_data["Total Quizzes"] = sum_of_quiz_scores / sum_of_quiz_max

average_quiz_scores = (quiz_scores / quiz_max_points).sum(axis=1) / len(quiz_max_points)
final_data["Average Quizzes"] = average_quiz_scores

final_data["Quiz Score"] = final_data[["Total Quizzes", "Average Quizzes"]].max(axis=1)

#Calculating the Final Score:
weightings = pd.Series(
    {
        "Exam 1": 0.05,
        "Exam 2": 0.1,
        "Exam 3": 0.15,
        "Quiz Score": 0.30,
        "Homework Score": 0.4,
    }
)

final_data["Final Score"] = final_data[weightings.index].multiply(weightings, axis=1).sum(axis=1)

#Rounding Up the Final Score:
final_data["Ceiling Score"] = np.ceil(final_data["Final Score"] * 100)

#Defining Grade Mapping:
grades = {
    90: "A",
    80: "B",
    70: "C",
    60: "D",
    0: "F",
}

def grade_mapping(value):
    for threshold, letter_grade in grades.items():
        if value >= threshold:
            return letter_grade
    return 'F'  

letter_grades = final_data["Ceiling Score"].apply(grade_mapping)
final_data["Final Grade"] = letter_grades

#Processing Data by Sections:
for section, table in final_data.groupby("Section"):
    sorted_table = table.sort_values(by=["Last Name", "First Name"])
    file_path = DATA_FOLDER / f'Section {section} Grades.csv'
    sorted_table.to_csv(file_path)
    
    num_students = sorted_table.shape[0]
    print(f"Section {section} - Number of Students: {num_students}")
    print(f"File Path: {file_path}")



#Visualizing Grade Distribution: Get Grade Counts and use plot to plot the grades
grade_counts = final_data["Final Grade"].value_counts().sort_index()
all_grades = ['A', 'B', 'C', 'D', 'F']
grade_counts = grade_counts.reindex(all_grades, fill_value=0)


grade_counts.plot(kind='bar')
plt.title("Grade Distribution")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)
plt.show()




final_mean = final_data["Final Score"].mean()
final_std = final_data["Final Score"].std()
x = np.linspace(final_mean - 5*final_std, final_mean + 5*final_std, 100)
plt.plot(x, scipy.stats.norm.pdf(x, final_mean, final_std), label="Normal Distribution", linewidth=2)
final_data["Final Score"].plot.hist(bins=20, alpha=0.7, label="Histogram")
final_data["Final Score"].plot.density(linewidth=4, label="Kernel Density Estimate")
plt.title("Final Score Distribution with Normal Curve")
plt.legend()
plt.show()


print("Grade Counts:\n", grade_counts)
print("mean = ", final_mean)
print("std = ", final_std)

