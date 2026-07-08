from typing import Optional

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
# FIXED: The original line `pd.concat([data, data['Phone'].astype('str')])` concats a Series
# as a new ROW (axis=0), which corrupts the DataFrame by adding a garbage row.
# Instead, convert the Phone column to string properly:
#   - Phone has NaN → read as float64 → direct .astype(str) gives "9099650224.0"
#   - Convert through Int64 (nullable integer) first to strip the ".0", then to string
data['Phone'] = data['Phone'].astype('Int64').astype('str')
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
# a) Count of workers by Work Permit, sorted descending
# Using value_counts() is more idiomatic than groupby+agg for simple counting
print(data['Work Permit'].value_counts().sort_values(ascending=False))

# b) Proportion (percentage) of workers who have a car vs. don't
# FIXED: .rename({'Name': 'Percentage'}) without axis= defaults to renaming the INDEX, not the column.
# Must use .rename(columns={...}) to rename the column properly.
car_ownership_counts = data.groupby(by='Has Car').agg({'Name': 'count'})
car_ownership_percentage = car_ownership_counts.rename(columns={'Name': 'Percentage'}) / data.shape[0] * 100.0
print(car_ownership_percentage)

# c) 5 most common Cities and their counts
# FIXED: Use value_counts() for clarity; nlargest would also work here
print(data['City'].value_counts().head(5))

# ---------------------------------------------------------------------------
# Q4: STRING OPERATIONS & FILTERING
#   a) Print the names and phone numbers of all workers whose Work Experience
#      mentions "forklift" (case-insensitive).
#   b) Print the number of workers who speak Spanish (hint: check the Languages column).
#   c) Create a new column 'Num_Roles' that counts how many role types each worker
#      selected. Print the worker with the most roles and how many they have.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
# a) Names and phone numbers of workers whose Work Experience mentions "forklift"
# FIXED: Use a list ['Name', 'Phone'] instead of a tuple ('Name', 'Phone') for column selection.
# Tuples work by accident for single-level columns but are meant for MultiIndex columns.
print(data[data['Work Experience'].str.contains('forklift', case=False, na=False)][['Name', 'Phone']])

# b) Number of workers who speak Spanish
# FIXED: Added case=False (default case=True misses capitalized "Spanish") and na=False (handle NaN).
# A simpler approach: str.contains('spanish', case=False, na=False) matches any casing.
spanish_speakers = data['Languages'].str.contains('spanish', case=False, na=False)
print(f"Workers who speak Spanish: {spanish_speakers.sum()}")

# c) Create 'Num_Roles' column counting role types; print worker with most roles
# FIXED: Column name now matches the question ('Num_Roles' not 'Num Roles').
# Also print both the worker's name AND how many roles they have.
# NOTE: All 437 workers in this dataset have exactly 5 roles, so we limit output to head().
data['Num_Roles'] = data['Role Types'].str.split(',').str.len()
max_num_roles = data['Num_Roles'].max()
top_workers = data[data['Num_Roles'] == max_num_roles][['Name', 'Num_Roles']]
print(f"Worker(s) with the most roles ({max_num_roles}):")
print(top_workers.head(10))
if len(top_workers) > 10:
    print(f"... and {len(top_workers) - 10} more workers with the same count")

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
# c) Number of workers who joined in each month, sorted by month
print(data.groupby(by='Join_Month').agg({'Name': 'count'}).sort_values(by='Join_Month'))
# d) Date of the most recent join
# FIXED: Use .max() instead of sorting the entire column and picking iloc[0].
# .max() is clearer and O(n) instead of O(n log n).
print(data['Joined'].max())

# ---------------------------------------------------------------------------
# Q6: GROUPBY & AGGREGATION
#   a) Group by 'State' and print the count and average Commute Distance per state.
#   b) Group by both 'Gender' and 'Has Car', and print:
#        - count of workers
#        - average Commute Distance
#        - average age (calculate age as 2026 - Birthday Year)
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
# a) Group by State: count and average Commute Distance per state
# FIXED: Added 'Name': 'count' — the original only showed mean, missing the requested count.
print(data.groupby(by='State').agg(
    Worker_Count=('Name', 'count'),
    Avg_Commute_Distance=('Commute Distance', 'mean')
))

# b) Group by Gender and Has Car: count, avg commute distance, avg age
# NOTE: Computing 2026 - mean(Birthday Year) is mathematically equivalent to mean(age)
# because of linearity of expectation: E[2026 - BY] = 2026 - E[BY]. Correct but non-obvious.
gender_has_car_group = data.groupby(by=['Gender', 'Has Car']).agg(
    Worker_Count=('Name', 'count'),
    Avg_Commute_Distance=('Commute Distance', 'mean'),
    Avg_Birthday_Year=('Birthday Year', 'mean')
)
gender_has_car_group['Avg_Age'] = 2026 - gender_has_car_group['Avg_Birthday_Year']
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
def get_commute_category(dist: float):
    if dist < 20:
        return "Short"
    elif dist < 50:
        return "Medium"
    return "Long"

def lang_count(languages: Optional[str]):
    # Handle NaN/None and non-string values
    if not isinstance(languages, str):
        return 0
    # Split by comma and count; strip whitespace for robustness
    return len([lang.strip() for lang in languages.split(',') if lang.strip()])

# a) Create Commute_Category column
# FIXED: Use .apply() instead of .transform(). While both work element-wise on a Series,
# the question explicitly asks for .apply(). .transform() is typically used with groupby.
data['Commute_Category'] = data['Commute Distance'].apply(get_commute_category)

# b) Print value_counts of Commute_Category
# FIXED: Use value_counts() directly as the question asks, instead of groupby+agg.
print(data['Commute_Category'].value_counts())

# c) Create Num_Languages — count languages per worker; print top 5 values
data['Num_Languages'] = data['Languages'].apply(lang_count)
# FIXED: The original printed data['Languages'].head() (wrong column) and then
# data['Num_Languages'].head(5) (first 5 rows, not top 5 values).
# "Top 5 values" means the most frequent counts — use value_counts().
print(data['Num_Languages'].value_counts().head(5))

# ---------------------------------------------------------------------------
# Q8: SORTING & RANKING
#   a) Print the 5 oldest workers (Name, Birthday Year, City).
#   b) Print the 3 workers with the longest commute (Name, City, Commute Distance).
#   c) Add a 'Commute_Rank' column that ranks workers by Commute Distance
#      (descending: rank 1 = longest commute). Handle ties with 'min' method.
#      Print the top 10 by this rank.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
# a) 5 oldest workers (smallest Birthday Year = oldest)
# FIXED: Use list [...] instead of tuple (...) for column selection.
print(data.sort_values(by='Birthday Year').head()[['Name', 'Birthday Year', 'City']])

# b) 3 workers with the longest commute
# FIXED: Use list instead of tuple for column selection.
print(data.sort_values(by='Commute Distance', ascending=False).head(3)[['Name', 'City', 'Commute Distance']])

# c) Add Commute_Rank column (descending: rank 1 = longest commute, ties use 'min' method)
# FIXED: This entire section was missing. rank() with ascending=False gives rank 1 to the
# largest value. method='min' gives tied values the same (minimum) rank.
data['Commute_Rank'] = data['Commute Distance'].rank(ascending=False, method='min').astype(int)
print("Top 10 by Commute Rank (1 = longest commute):")
print(data.sort_values(by='Commute_Rank')[['Name', 'City', 'Commute Distance', 'Commute_Rank']].head(10))


# ---------------------------------------------------------------------------
# Q9: PIVOT & CROSSTAB
#   a) Create a pivot table showing the mean Commute Distance for each
#      combination of 'Has Car' and 'Work Permit'. Print it.
#   b) Create a crosstab showing the count of workers by Gender vs Has Car.
#      Print it.
# ---------------------------------------------------------------------------

# YOUR ANSWER HERE
# a) Pivot table: mean Commute Distance for each combination of Has Car and Work Permit
# FIXED: Use pivot_table() as the question asks, not groupby+agg.
# pivot_table() produces a 2D grid with one dimension as rows, the other as columns.
pivot = data.pivot_table(
    index='Has Car',
    columns='Work Permit',
    values='Commute Distance',
    aggfunc='mean'
)
print("Mean Commute Distance by Has Car × Work Permit:")
print(pivot)

# b) Crosstab: count of workers by Gender vs Has Car
# FIXED: This section was entirely missing. pd.crosstab() creates a contingency table.
crosstab = pd.crosstab(data['Gender'], data['Has Car'])
print("\nWorker count by Gender × Has Car:")
print(crosstab)

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
# a) Create summary DataFrame: group by City, calculate worker count and avg commute.
#    Only include cities with at least 3 workers.
# FIXED:
#   - .rename() without axis= defaults to renaming the INDEX, not columns.
#     Use .rename(columns={...}) to rename columns.
#   - The filter (>= 3 workers) must be applied TO the summary, not just in a print.
#   - Use the new column name 'City_Count' for filtering, not the old 'Name'.
summary = data.groupby(by='City').agg(
    City_Avg_Commute=('Commute Distance', 'mean'),
    City_Worker_Count=('Name', 'count')
)
# Filter to cities with at least 3 workers
summary = summary[summary['City_Worker_Count'] >= 3]
print("City summary (>= 3 workers):")
print(summary)

# b) Merge the summary back to the original data on City (left join)
# FIXED: data.join() returns a NEW DataFrame — the original was lost because it wasn't assigned.
merged = data.join(summary, on='City', how='left')

# c) Print 5 random rows showing Name, City, City_Worker_Count, City_Avg_Commute
# FIXED: The original printed data.head() (first 5 rows, wrong DataFrame).
# Use .sample(random_state=42) for 5 reproducible random rows from the merged result.
print("\n5 random rows from merged result (random_state=42):")
print(merged[['Name', 'City', 'City_Worker_Count', 'City_Avg_Commute']].sample(5, random_state=42))

# =============================================================================
# VERIFICATION — run this block to check your answers are producing output.
# It does NOT check correctness; it just confirms your code runs without error
# and prints something for each question.
# =============================================================================
print("\n" + "=" * 60)
print("All 10 questions executed. Review the output above for correctness.")
print("=" * 60)
