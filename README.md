
# Cleaning The Data

There were 4 data quality checks done:
 1. Deleting rows with missing values: There were 2 rows which were empty that have been deleted
 2. Check for duplicates: There were no duplicate values
 3. Converting Cost Columns to numeric: The Accommodation ad Transportation values had a mix of $ and USD next to the values, which pandas might read as text, so they were removed
 4. Changing Start and End Date to datetime format: The format of the dates are m/d/y, which pandas sees as a string. The correct format is y-m-d, which it has been converted into
 4. In the transportation type columns, the passengers who travelled by plane were also written as 'flight' and 'airplane'. So 'flight' and 'airplane' were converted to plane, so that all passengers who travelled by plane appeared togther.
 
The data cleaning was done in python notebook, to see results for each data quality check done. The streamlit app is in the .py file. 


# Running the App

In the terminal, type 'streamlit run Travel_Dashboard.py' 
