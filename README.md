Step-by-Step Tasks
1.1.  Part 1: Data Loading and Basic Exploration (2-3 hours)

    - Download and load the data

    - Download only the metadata.csv file from the CORD-19 dataset

    - Load it into a pandas DataFrame

    - Examine the first few rows and data structure

1.2. Basic data exploration

    - Check the DataFrame dimensions (rows, columns)

    - Identify data types of each column

    - Check for missing values in important columns

    - Generate basic statistics for numerical columns

2.1. Part 2: Data Cleaning and Preparation (2-3 hours)

    - Handle missing data

    - Identify columns with many missing values

    - Decide how to handle missing values (removal or filling)

    - Create a cleaned version of the dataset

    - Prepare data for analysis

    - Convert date columns to datetime format

    - Extract year from publication date for time-based analysis

    - Create new columns if needed (e.g., abstract word count)

Part 3: Data Analysis and Visualization (3-4 hours)

Perform basic analysis

Count papers by publication year

Identify top journals publishing COVID-19 research

Find most frequent words in titles (using simple word frequency)

Create visualizations

Plot number of publications over time

Create a bar chart of top publishing journals

Generate a word cloud of paper titles

Plot distribution of paper counts by source

Part 4: Streamlit Application 

Build a simple Streamlit app

Create a basic layout with title and description

Add interactive widgets (sliders, dropdowns)

Display your visualizations in the app

Show a sample of the data

Example app structure:

python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Add interactive elements
year_range = st.slider("Select year range", 2019, 2022, (2020, 2021))
# Add visualizations based on selection
Part 5: Documentation and Reflection

Document your work

Write comments in your code

Create a brief report of your findings

Reflect on challenges and learning

Evaluation Criteria

Your project will be evaluated based on:

Complete implementation (40%): All tasks completed

Code quality (30%): Readable, well-commented code

Visualizations (20%): Clear, appropriate charts

Streamlit app (10%): Functional application

Tips for Success

Start small: Begin with a subset of the data if the full file is too large

Focus on basics: Don't worry about advanced analysis techniques

Debug incrementally: Test each part of your code as you write it

Use resources: Consult pandas and Streamlit documentation when stuck

Ask for help: Reach out to instructors or peers if you get stuck

Example Code Snippets
python
# Load the data
import pandas as pd
df = pd.read_csv('metadata.csv')

# Basic info
print(df.shape)
print(df.info())

# Check missing values
print(df.isnull().sum())