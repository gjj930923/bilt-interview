import pandas as pd
import numpy as np

# =============================================================================
# PANDAS EXERCISE — 10 Questions based on full_unique_workers_20260614.csv
# =============================================================================
# Write your answer below each question. Run the file to verify correctness.
# The dataset contains worker profiles: demographics, work permits, languages,
# commute info, availability, role types, and work experience.
# =============================================================================

# Load the data
data = pd.read_csv('full_unique_workers_20260614.csv')
data = pd.concat([data, data['Phone'].astype('str')])
# =============================================================================
# WARM-UP EXAMPLE: Find the 2nd oldest worker
# =============================================================================
# Calculate age first, then we can approach it a few ways:
ages = 2026 - data['Birthday Year']

# Method 1: drop_duplicates to handle ties, sort, then pick with iloc
second_oldest_age = ages.drop_duplicates().sort_values(ascending=False).iloc[1]
print(f"2nd oldest age: {second_oldest_age}")
print(data[ages == second_oldest_age][['Name', 'Birthday Year', 'City']])

# Method 2: using nlargest (returns rows, not just ages)
# data_with_age = data.copy()
# data_with_age['Age'] = 2026 - data_with_age['Birthday Year']
# print(data_with_age.nlargest(2, 'Age').iloc[-1][['Name', 'Age', 'City']])

# ---------------------------------------------------------------------------
# Q1: INITIAL EXPLORATION
# Use info() and describe() to understand the dataset structure.
# Then print:
#   - The total number of rows and columns
#   - The data types of all columns
#   - Summary statistics for all numeric columns
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
print(data.info())
print(data.describe())

# ---------------------------------------------------------------------------
# Q2: MISSING DATA
# Some columns have missing values.
#   a) Print the count of missing values in each column, sorted from most to least missing.
#   b) Print the percentage of rows where Email is missing.
#   c) Create a new DataFrame that drops all rows where ANY of the availability
#      columns (Weekday Start, Weekday End, Weekend Start, Weekend End) are missing.
#      Print its shape.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
print(data.isna().sum().sort_values(ascending=False))
print(f"{data['Email'].isna().sum() / data.shape[0] * 100.0}%")
df_with_availability = data.dropna(subset=["Weekday Start", "Weekday End", "Weekend Start", "Weekend End"])
print(df_with_availability.shape)

# ---------------------------------------------------------------------------
# Q3: VALUE COUNTS & PROPORTIONS
#   a) Print the count of workers by Work Permit category, sorted descending.
#   b) Print the proportion (percentage) of workers who have a car vs. don't.
#   c) Print the 5 most common Cities and their counts.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
print(data.groupby(by='Work Permit').agg({'Name': 'count'}).rename(columns={'Name': 'Cnt'}).sort_values(by='Cnt', ascending=False))
car_ownership_percentage = data.groupby(by='Has Car').agg({'Name': 'count'}).rename({'Name': 'Percentage'}) / data.shape[0] * 100.0
print(car_ownership_percentage)
cities = data.groupby(by='City').agg({'Name': 'count'}).nlargest(5, 'Name')
print(cities)

# ---------------------------------------------------------------------------
# Q4: STRING OPERATIONS & FILTERING
#   a) Print the names and phone numbers of all workers whose Work Experience
#      mentions "forklift" (case-insensitive).
#   b) Print the number of workers who speak Spanish (hint: check the Languages column).
#   c) Create a new column 'Num_Roles' that counts how many role types each worker
#      selected. Print the worker with the most roles and how many they have.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
print(data[data['Work Experience'].str.contains('forklift', case=False)].loc[:,('Name', 'Phone')])
print(data['Languages'].str.contains('spanish').sum())
data['Num Roles'] = data['Role Types'].str.split(',').str.len()
max_num_roles = data['Num Roles'].max()
print(data[data['Num Roles'] == max_num_roles].loc[:,'Name'])

# ---------------------------------------------------------------------------
# Q5: DATE/TIME TRANSFORMATIONS
# The 'Joined' column is in YYYYMMDD format.
#   a) Convert 'Joined' to a proper datetime column.
#   b) Extract the join-month (1-12) and create a new column 'Join_Month'.
#   c) Print the number of workers who joined in each month, sorted by month.
#   d) Print the date of the most recent join.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
data['Joined'] = pd.to_datetime(data['Joined'], format='%Y%m%d')
data['Join_Month'] = data['Joined'].dt.month
print(data.groupby(by='Join_Month').agg({'Name': 'count'}).sort_values(by='Join_Month'))
print(data['Joined'].sort_values(ascending=False).iloc[0])

# ---------------------------------------------------------------------------
# Q6: GROUPBY & AGGREGATION
#   a) Group by 'State' and print the count and average Commute Distance per state.
#   b) Group by both 'Gender' and 'Has Car', and print:
#        - count of workers
#        - average Commute Distance
#        - average age (calculate age as 2026 - Birthday Year)
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
print(data.groupby(by='State').agg({'Commute Distance': 'mean'}))
gender_has_car_group = data.groupby(by=['Gender', 'Has Car']).agg({'Name': 'count', 'Commute Distance': 'mean', 'Birthday Year': 'mean'})
gender_has_car_group['Age'] = 2026 - gender_has_car_group['Birthday Year']
print(gender_has_car_group)

# ---------------------------------------------------------------------------
# Q7: APPLY & CUSTOM FUNCTIONS
#   a) Write a function that classifies Commute Distance as:
#        'Short' (< 20 miles), 'Medium' (20-49 miles), 'Long' (50+ miles).
#      Create a new column 'Commute_Category' using this function via .apply().
#   b) Print a value_counts of Commute_Category.
#   c) Use .apply() on the 'Languages' column to create 'Num_Languages' —
#      the number of languages each worker speaks. Print the top 5 values.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE


# ---------------------------------------------------------------------------
# Q8: SORTING & RANKING
#   a) Print the 5 oldest workers (Name, Birthday Year, City).
#   b) Print the 3 workers with the longest commute (Name, City, Commute Distance).
#   c) Add a 'Commute_Rank' column that ranks workers by Commute Distance
#      (descending: rank 1 = longest commute). Handle ties with 'min' method.
#      Print the top 10 by this rank.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE


# ---------------------------------------------------------------------------
# Q9: PIVOT & CROSSTAB
#   a) Create a pivot table showing the mean Commute Distance for each
#      combination of 'Has Car' and 'Work Permit'. Print it.
#   b) Create a crosstab showing the count of workers by Gender vs Has Car.
#      Print it.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE


# ---------------------------------------------------------------------------
# Q10: MERGE / JOIN & BONUS ANALYSIS
#   a) From the original data, create a summary DataFrame: group by City and
#      calculate the worker count and average Commute Distance. Only include
#      cities with at least 3 workers.
#   b) Merge this summary back to the original data on City (left join).
#   c) Print 5 random rows showing Name, City, City_Worker_Count, and
#      City_Avg_Commute from the merged result (use random_state=42).
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE


# =============================================================================
# VERIFICATION — run this block to check your answers are producing output.
# It does NOT check correctness; it just confirms your code runs without error
# and prints something for each question.
# =============================================================================
print("\n" + "=" * 60)
print("All 10 questions executed. Review the output above for correctness.")
print("=" * 60)
