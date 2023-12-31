import streamlit as st
import pandas as pd

# Function to get disbursement quarter
def get_disbursement_quarter(df):
    df['DisburseQuarter'] = (df['DisburseDate'].dt.quarter + 2) % 4 + 1
    return df

# Function to get due quarter
def get_due_quarter(df):
    df['DueQuarter'] = (df['RealizedDate'].dt.quarter + 2) % 4 + 1
    return df

# Function to calculate number of loans for each period
def loans_per_quarter(df1, df2):
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

# Function to calculate DPD per quarter
def dpd_per_quarter(visual_df, df2, filter_val):
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
    
    filter_val = int(filter_val)

    for index, row in df2.iterrows():
        if (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 1) & (row['DPD'] >= filter_val):
            Q1_1 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 2) & (row['DPD'] >= filter_val):
            Q1_2 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 3) & (row['DPD'] >= filter_val):
            Q1_3 += 1
        elif (row['DisburseQuarter'] == 1) & (row['DueQuarter'] == 4) & (row['DPD'] >= filter_val):
            Q1_4 += 1
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 2) & (row['DPD'] >= filter_val):
            Q2_2 += 1
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 3) & (row['DPD'] >= filter_val):
            Q2_3 += 1 
        elif (row['DisburseQuarter'] == 2) & (row['DueQuarter'] == 4) & (row['DPD'] >= filter_val):
            Q2_4 += 1
        elif (row['DisburseQuarter'] == 3) & (row['DueQuarter'] == 3) & (row['DPD'] >= filter_val):
            Q3_3 += 1
        elif (row['DisburseQuarter'] == 3) & (row['DueQuarter'] == 4) & (row['DPD'] >= filter_val):
            Q3_4 += 1
        elif (row['DisburseQuarter'] == 4) & (row['DueQuarter'] == 4) & (row['DPD'] >= filter_val):
            Q4_4 += 1
    visual_df['Q1'] = [Q1_1, 0, 0, 0]
    visual_df['Q2'] = [Q1_2, Q2_2, 0, 0]
    visual_df['Q3'] = [Q1_3, Q2_3, Q3_3, 0]
    visual_df['Q4'] = [Q1_4, Q2_4, Q3_4, Q4_4]
    return visual_df

# Main Streamlit app
def main():
    st.title("Buro BD DPD-Dashboard")

    # Read and drop null rows
    df = pd.read_excel("DPD_Sample.xlsx") ## CHANGE FILE PATH HERE
    df = df.dropna()

    # Get disbursement and due quarters
    df = get_disbursement_quarter(df)
    df = get_due_quarter(df)

    # Create new DataFrame for visualization purposes
    visual_df = pd.DataFrame(
        {"DisbursePeriod": ["Q1-FY22-23", "Q2-FY22-23", "Q3-FY22-23", "Q4-FY22-23"]}
    )

    # Calculate number of loans for each period
    visual_df = loans_per_quarter(df, visual_df)

    # Sort DataFrame by 'LoaneeNo' and 'DisburseDate'
    df.sort_values(['LoaneeNo', 'RealizedDate'], inplace=True)

    # Streamlit web app loop
    with st.form(key='my_form'):
        # Add buttons for predefined filter values with unique keys
        filter_choice = st.radio("Select DPD Filter:", ["7+ DPD", "30+ DPD", "60+ DPD"], key="filter_choice")

        # Calculate and display the visual DataFrame
        visual_df = dpd_per_quarter(visual_df, df, filter_choice.split('+')[0].strip())
        st.write(visual_df)

        # Add a submit button to trigger the form
        submit_button = st.form_submit_button(label='Submit')

if __name__ == "__main__":
    main()
