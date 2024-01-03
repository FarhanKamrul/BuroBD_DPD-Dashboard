#!/usr/bin/env python3

'''
The dataset (excel) is formatted as follows:

| BranchCode | LoaneeNo | ItemCode | LoanTerm | DisburseDate | ReportDate | RealizableDate | RealizedDate | RealizableAmt | RealizedAmt | PaymentFrequency | DPD |
|------------|----------|----------|----------|--------------|------------|----------------|--------------|---------------|-------------|------------------|-----|


We ought to create another table that looks like (the values are simply placeholders):

| DisbursePeriod | NumberOfLoans | Q1 | Q2 | Q3 | Q4 |
|----------------|---------------|----|----|----|----|
| Q1-FY22-23     | 5194          | 28 | 0  | 0  | 0  |
| Q2-FY22-23     | 36802         | 0  | 1  | 14 | 45 |
| Q3-FY22-23     | 40857         | 0  | 0  | 6  | 35 |
| Q4-FY22-23     | 23628         | 0  | 0  | 0  | 3  |

**The values are placeholders.

Required buttons: 7+ DPD, 15+ DPD, 30+ DPD, 60+ DPD, 90+ DPD


The idea is to calculate how many loans disbursed in Q(1-4)-FY22-23 are still due at the end of Q1, Q2, Q3, Q4 of the same fiscal year


Algorithm (high level):
- Convert | DisburseDate | ReportDate | RealizableDate | RealizedDate | to datetime() format
- Drop all entries not in the 2022-23 Fiscal Year (July 1, 2022 to June 30, 2023)
- Assign a UID (Unique Loanee ID) by concatenating LoaneeNo, Itemcode and LoanTerm.
- For each UID, only keep the last transaction at the end of each quarters. Drop the rest.
- Create a new dataframe that looks like the following: 
| DisbursePeriod | NumberOfLoans |
| Q1-FY22-23     | |
| Q2-FY22-23     | |
| Q3-FY22-23     | |
| Q4-FY22-23     | |

**Number of loans indicate number of loans disbursed in that period. 
- Ask for a DPD value
- Print the table after calculations

'''
import pandas as pd
import streamlit as st

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
    df['DueQuarter'] = df['ReportDate'].apply(assign_quarter)
    return df

def drop_duplicates(df):
    return df.drop_duplicates(subset=['UID', 'DueQuarter'], keep='last')

def create_visualization_df():
    return pd.DataFrame({"DisbursePeriod": ["Q1-FY22-23", "Q2-FY22-23", "Q3-FY22-23", "Q4-FY22-23"]})

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

    df2['NumberOfLoans'] = [Q1, Q2, Q3, Q4]
    return df2


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
    st.set_page_config(
        page_title = "Vintage Analysis Dashboard FY22-23",
        page_icon = ":chart_increasing:",
        layout = "wide",
    )

    st.title("Vintage Analysis Dashboard FY22-23")

    # Loading the Dataset
    file_path = 'DPD_Sample.xlsx'
    df = load_and_preprocess_data(file_path)

    # Setting up sidebar
    st.sidebar.header("Filter")
    options = ['7+ DPD', '15+ DPD', '30+ DPD', '60+ DPD', '90+ DPD']
    number_mapping = {option: int(option.split('+')[0].strip()) for option in options}
    selected_option = st.sidebar.radio("Select a filter:", options)
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


