
import pandas as pd
import streamlit as st


# Loading the dataset
df = pd.read_csv("/Users/anamleen/Desktop/Travel details dataset.csv") 

st.title("Travel Dashboard")

# Data Cleaning

# Check 1 : Remove rows with missing values
df = df.dropna()

# Check 2: Dropping Duplicate rows
df = df.drop_duplicates() 

# Check 3: Convert cost columns to numeric 
for col in ["Accommodation cost", "Transportation cost"]:
    df[col] = df[col].astype(str).str.replace(r"[^0-9.]", "", regex=True)
    df[col] = pd.to_numeric(df[col])


# Check 4: Convert the date text into real dates (month/day/year)
df["Start date"] = pd.to_datetime(df["Start date"], format="%m/%d/%Y")
df["End date"] = pd.to_datetime(df["End date"], format="%m/%d/%Y")

# Check 5: Convert Flight and Airplane to Plane in the Transportation Type column
df["Transportation type"] = df["Transportation type"].replace({
    "Airplane": "Plane",
    "Flight": "Plane"
})

# Add Year and Total cost columns
df["Year"] = df["Start date"].dt.year
df["Total cost (USD)"] = df["Accommodation cost"] + df["Transportation cost"]

# Remove 00:00:00 from date columns
df["Start date"] = df["Start date"].dt.date
df["End date"] = df["End date"].dt.date


# Streamlit Layout
st.sidebar.header("Search")
name = st.sidebar.text_input("Passenger name")
destination = st.sidebar.text_input("Destination")
accomodation = st.sidebar.selectbox("Accommodation type", ["All"] + sorted(df["Accommodation type"].unique()))
transportation = st.sidebar.selectbox("Transportation type", ["All"] + sorted(df["Transportation type"].unique()))
year = st.sidebar.selectbox("Year", ["All"] + sorted(df["Year"].unique().tolist()))

results = df

if name:
    results = results[results["Traveler name"].str.contains(name, case=False, regex=False)]
if destination:
    results = results[results["Destination"].str.contains(destination, case=False, regex=False)]
if accomodation != "All":
    results = results[results["Accommodation type"] == accomodation]
if transportation != "All":
    results = results[results["Transportation type"] == transportation]
if year != "All":
    results = results[results["Year"] == year]

# Metrics 
col1, col2, col3 = st.columns(3)
col1.metric("Total trips", len(results))
col2.metric("Different travellers", results["Traveler name"].nunique())
col3.metric("Total spend (USD)", f"{results['Total cost (USD)'].sum():,.0f}")



if len(results) == 0:
    st.warning("No trips found. Try a different search.")
else:
      # The table
    st.subheader("Trip details")
    st.dataframe(results.drop(columns="Year"), hide_index=True)

    # The chart
    st.subheader("Chart")
    chart_by = st.selectbox("Show total spend by", ["Accommodation type", "Transportation type", "Year"])
    chart_data = results.groupby(chart_by)["Total cost (USD)"].sum()
    st.bar_chart(chart_data)