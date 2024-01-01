#!/usr/bin/env python3
import streamlit as st 
import pandas as pd 

# Function Definitions
def get_disbursement_quarter(df):
    df['DisburseQuarter'] = (df['DisburseDate'].dt.quarter+2)%4+1
    return df

def get_due_quarter(df):
    df['DueQuarter'] = (df['RealizedDate'].dt.quarter+2)%4+1
    return df 

def loansPerQuarter(df1, df2):
    Q1 = 0
    Q2 = 0
    Q3 = 0
    Q4 = 0

    for index, row in df1.iterrows():
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

# Main Function
def main():
    st.title("Buro BD DPD-Dashboard")
    df = pd.read_excel("DPD_Sample.xlsx")
    df = df.dropna()

    df = get_disbursement_quarter(df)
    df = get_due_quarter(df)

    visualDf = pd.DataFrame(
        {
            "DisbursePeriod" : ["Q1-FY22-23","Q2-FY22-23","Q3-FY22-23","Q4-FY22-23"]
        }
    )

    visualDf = loansPerQuarter(df, visualDf)

    df2 = df
    df2.sort_values(['LoaneeNo', 'RealizedDate'], inplace=True)
    # Assuming 'LoaneeNo' and 'DueQuarter' uniquely identify each loan in a given quarter
    # Idea is that we only count the ending DPD value per quarter for each loanee.
    df2 = df2.drop_duplicates(subset=['LoaneeNo', 'DueQuarter'], keep='last')


    filterVal = st.sidebar.radio("Select DPD Filter Value", [7, 15, 30, 60, 90])

    visualDf = dpdPerQuarter(visualDf, df2, filterVal)
    st.write(visualDf)


# Call the main function
if __name__ == "__main__":
    main()

