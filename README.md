# Grade Data Analyzer

## Overview

This Python script calculates student grades by integrating data from multiple sources, including class rosters, homework & exam grades, and quiz grades. It utilizes Pandas, NumPy, Matplotlib, and SciPy for data handling and analysis.

## Prerequisites

Before running the script, ensure the following are installed:

- Python
- Required Python libraries:
  - Pandas
  - NumPy
  - Matplotlib
  - SciPy

  Install these libraries using pip:
```bash
  pip install pandas numpy matplotlib scipy
```

## Data Preparation

Your data files should be placed in a directory named `data` within the same directory as the script. The script expects these files:
- `roster.csv` for class roster.
- `hw_exam_grades.csv` for homework and exam grades.
- `quiz_[1-5]_grades.csv` for quiz grades.

## Running the Script in Bash

To run the script in a Bash environment, follow these steps:

1. Open your terminal.
2. Clone the repo
``` bash
   git clone https://github.com/antenmanuuel/GradesDataAnalyzer.git
```
3. Navigate to the directory containing the script:
```bash
  cd GradesDataAnalyzer
```
4. Execute the script:
```bash
  python data_base.py
```


## Output

The script will produce:
- CSV files for each section with student grades.
- Visual plots of grade distributions.
- Console output showing statistical metrics like mean and standard deviation of final scores.

## Customization

Adjust weightings, grading scales, and other parameters in the script as needed to fit different grading schemes.

## Troubleshooting

If you encounter issues:
- Check that all data files are correctly formatted and located in the `data` directory.
- Verify the installation of all required Python libraries.
- Review the script for syntax or logical errors.

---

*Note: This script is intended for educational purposes and requires specific data formats to function correctly.*
