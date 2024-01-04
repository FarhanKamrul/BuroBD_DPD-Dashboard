#!/usr/bin/env python3

'''
This Streamlit app is designed to perform a detailed analysis of vintage data extracted from a loan dataset, structured as an Excel file. The dataset comprises various columns such as BranchCode, LoaneeNo, ItemCode, LoanTerm, DisburseDate, ReportDate, RealizableDate, RealizedDate, RealizableAmt, RealizedAmt, PaymentFrequency, and DPD (Days Past Due).

## Objective:
The primary goal of the app is to generate a new table showcasing the number of loans disbursed in each quarter of the Fiscal Year 2022-23 (Q1-FY22-23 to Q4-FY22-23). Additionally, the app calculates the count of loans with Days Past Due (DPD) exceeding specific thresholds (7+, 15+, 30+, 60+, 90+ DPD).

## Algorithm (High-level):
1. Convert date columns (DisburseDate, ReportDate, RealizableDate, RealizedDate) to datetime format.
2. Filter data to include only entries within the 2022-23 Fiscal Year (July 1, 2022, to June 30, 2023).
3. Assign a Unique Loanee ID (UID) by concatenating LoaneeNo, Itemcode, and LoanTerm.
4. Retain only the last transaction for each UID at the end of each quarter; discard the rest.
5. Create a new DataFrame summarizing the number of loans disbursed in each quarter.

## Visualization:
The app presents radio buttons for selecting DPD thresholds (7+, 15+, 30+, 60+, 90+ DPD). The resulting table displays the number of loans disbursed in each quarter along with the count of loans exceeding the chosen DPD threshold.

## Required Buttons:
- 7+ DPD
- 15+ DPD
- 30+ DPD
- 60+ DPD
- 90+ DPD

'''

import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    # Load your data
    df = pd.read_excel(file_path)
    
    # Convert dates to datetime format
    for col in ['DisburseDate', 'ReportDate', 'RealizableDate', 'RealizedDate']:
        df[col] = pd.to_datetime(df[col])

    return df

def filter_fiscal_year(df):
    # Filter for the 2022-23 Fiscal Year
    start_date = pd.to_datetime('2022-07-01')
    end_date = pd.to_datetime('2023-06-30')
    mask = (df['DisburseDate'] >= start_date) & (df['DisburseDate'] <= end_date)
    return df.loc[mask]

def assign_uid(df):
    # Assign a UID
    df['UID'] = df['LoaneeNo'].astype(str) + df['ItemCode'].astype(str) + df['LoanTerm'].astype(str)
    return df

def filter_by_fiscal_year(df):
    # Define the start and end of the fiscal year
    fy_start = pd.to_datetime("2022-07-01")
    fy_end = pd.to_datetime("2023-06-30")
    
    # Filter the DataFrame
    return df[(df['DisburseDate'] >= fy_start) & (df['DisburseDate'] <= fy_end) & 
              (df['ReportDate'] >= fy_start) & (df['ReportDate'] <= fy_end)]

def assign_quarter(date):
    if 1 <= date.month <= 3:
        return 3
    elif 4 <= date.month <= 6:
        return 4
    elif 7 <= date.month <= 9:
        return 1
    else:
        return 2

def add_quarters(df):
    df['DisburseQuarter'] = df['DisburseDate'].apply(assign_quarter)
    df['DueQuarter'] = df[['ReportDate', 'RealizableDate']].max(axis=1).apply(assign_quarter)
    return df

def drop_duplicates(df):
    return df.drop_duplicates(subset=['UID', 'DueQuarter'], keep='last')

@st.cache_data
def create_visualization_df():
    return pd.DataFrame({"Disburse Period": ["Q1-FY22-23", "Q2-FY22-23", "Q3-FY22-23", "Q4-FY22-23"]})

@st.cache_data
def calculate_loans_per_quarter(df1, df2):
    Q1, Q2, Q3, Q4 = 0, 0, 0, 0

    for _, row in df1.iterrows():
        if row['DisburseQuarter'] == 1:
            Q1 += 1
        elif row['DisburseQuarter'] == 2:
            Q2 += 1
        elif row['DisburseQuarter'] == 3:
            Q3 += 1
        else:
            Q4 += 1

    df2['Number of Loans'] = [Q1, Q2, Q3, Q4]
    return df2

@st.cache_data
def dpdPerQuarter(visualDf, df2, filterVal):
    Q1_1 = 0
    Q1_2 = 0
    Q1_3 = 0
    Q1_4 = 0
    Q2_2 = 0
    Q2_3 = 0
    Q2_4 = 0
    Q3_3 = 0
    Q3_4 = 0
    Q4_4 = 0
    
    filterVal = int(filterVal)

    for index, row in df2.iterrows():
        if (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 1) & (row['DPD'] >= filterVal):
            Q1_1 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 2) & (row['DPD'] >= filterVal):
            Q1_2 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 3) & (row['DPD'] >= filterVal):
            Q1_3 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 4) & (row['DPD'] >= filterVal):
            Q1_4 += 1
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 2) & (row['DPD'] >= filterVal):
            Q2_2 += 1
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 3) & (row['DPD'] >= filterVal):
            Q2_3 += 1 
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 4) & (row['DPD'] >= filterVal):
            Q2_4 += 1
        elif (row['DisburseQuarter'] == 3) & (row['DueQuarter'] == 3) & (row['DPD'] >= filterVal):
            Q3_3 += 1
        elif (row['DisburseQuarter'] == 3) & (row['DueQuarter'] == 4) & (row['DPD'] >= filterVal):
            Q3_4 += 1
        elif (row['DisburseQuarter'] == 4) & (row['DueQuarter'] == 4) & (row['DPD'] >= filterVal):
            Q4_4 += 1
    visualDf['Q1'] = [Q1_1, 0, 0, 0]
    visualDf['Q2'] = [Q1_2, Q2_2, 0, 0]
    visualDf['Q3'] = [Q1_3, Q2_3, Q3_3, 0]
    visualDf['Q4'] = [Q1_4, Q2_4, Q3_4, Q4_4]
    return visualDf

@st.cache_data
def load_and_preprocess_data(file_path):
    df = load_data(file_path)
    df = filter_fiscal_year(df)
    df = assign_uid(df)
    df = filter_by_fiscal_year(df)
    df = add_quarters(df)
    df = drop_duplicates(df)
    return df

def main():
    # Set up streamlit dashboard page
    image = "logo.png"
    st.set_page_config(
        page_title = "Vintage Analysis Dashboard FY22-23",
        page_icon = image,
        layout = "wide",
    )
    st.title(":gray[Vintage Analysis Dashboard FY22-23] :chart_with_upwards_trend:")

    # Loading the Dataset
    file_path = 'DPD_Sample.xlsx'
    df = load_and_preprocess_data(file_path)

    # Setting up columns
    col1, col2 = st.columns([1,3]) # Adjust the ratio as needed

    # Put the radio buttons in the first column
    with col1:
        options = ['7+ DPD', '15+ DPD', '30+ DPD', '60+ DPD', '90+ DPD']
        number_mapping = {option: int(option.split('+')[0].strip()) for option in options}
        selected_option = st.radio("DPD Value", options)

    # Put the rest of the dashboard in the second column
    with col2:
        # Initialize visualDf
        visual_df = create_visualization_df()
        visual_df = calculate_loans_per_quarter(df, visual_df)

        #Make it faster by making streamlit only rerun this part?
        filterVal = number_mapping[selected_option]
        # Calculate and print the visual DataFrame
        visual_df = dpdPerQuarter(visual_df, df, filterVal)

        st.dataframe(visual_df, hide_index=True)


if __name__ == "__main__":
    main()
