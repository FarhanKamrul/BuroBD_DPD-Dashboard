## Progress Report

🟩 - Complete
🟨 - Under Process
🟥 - Not started

- WebApp development complete. 🟩
- User Guide created. 🟩
- Logical inaccuracies handled according to feedback, needs review. 🟨
  - Calculating Due Quarter using max realizable date and report date, what does this mean? Do we include the latter date as the date when it is to be due? 🟨
- Testing feature accuracies 🟨
  - ```testcase1.xlsx``` assumes all loans are unique (using unique itemcodes for each). 🟩
  - Test *clumping*, i.e., the same loanee making multiple deposits on the same loan. 🟨
  - Test loans per quarter calculations 🟩
  - Test a large dataset with known vintage analysis 🟥
    OR
  - Perform vintage analysis on the existing sample manually and cross check. 🟥 

# DPD-Dashboard User Guide

## Introduction
This dashboard was constructed to automate the vintage analysis process for BURO Bangladesh. 

Vintage analysis, also known as cohort analysis, is a method used in credit risk management to evaluate the credit quality of a loan portfolio. The term 'Vintage' refers to the month or quarter in which an account was opened or a loan was granted.

In simple terms, vintage analysis measures the performance of a portfolio in different periods of time after the loan (or credit card) was granted. Performance can be measured in various ways, such as the cumulative charge-off rate, proportion of customers 30/60/90 days past due (DPD), utilization ratio, average balance, etc.

## Getting Started
1. **Download** the repository. Download the ```.streamlit``` file to the app root to enable custome themes. 
2. **Start the Dashboard:**
    - **WSL (Windows Subsystem for Linux):**
        ```bash
        streamlit run path/to/your/app/dpd_dashboard.py
        ```
    - **Mac/Linux:**
        ```bash
        streamlit run path/to/your/app/dpd_dashboard.py
        ```
3. **Access the Dashboard**: Paste the generated Local or Network URL on the browser address bar.
4. **Select DPD Filter Value:** On the sidebar, choose the DPD filter value from the radio buttons. You can select from 7, 15, 30, 60, or 90 days.

## Dashboard Sections

### Loans per Quarter
- **Description:** This section provides the number of loans disbursed in each quarter of the fiscal year.
- **Visualization:** A table with columns representing quarters (Q1 to Q4) and rows indicating the number of loans disbursed.

### DPD per Quarter
- **Description:** This section displays the count of loans with DPD values exceeding the selected filter value in each quarter.
- **Visualization:** A table with columns representing quarters (Q1 to Q4) and rows indicating the count of loans with DPD values above the selected threshold.

## Using the Dashboard

**Read the Data:** The data is loaded from the "DPD_Sample.xlsx" file. To use a different file, modify the file path in the script.
    - Example:
        ```python
        df = pd.read_excel("path/to/your/data/file.xlsx")
        ```
**Filter DPD Data:** Use the sidebar to choose the DPD filter value. This value determines the threshold for considering loans in the DPD analysis.

The table should look like the following:
| Disburse Period | Number of Loans | Q1 | Q2 | Q3 | Q4 |
|-----------------|-----------------|----|----|----|----|
| Q1-FY22-23      | 9999            | 22 | 33 | 44 | 55 |
| Q2-FY22-23      | 8888            | 0  | 66 | 77 | 88 |
| Q3-FY22-23      | 7777            | 0  | 0  | 99 | 111|
| Q4-FY22-23      | 6666            | 0  | 0  | 0  | 222|

**Number of Loans** indicate the *total* number of loans disbursed in that period.

**DPD (Days Past Due)** indicate the number of days a payment is overdue.

**Q1, Q2, Q3 and Q4** columns indicate the number of loans that exceed the threshold DPD value due in that quarter. The corresponding rows indicate the period in which those loans were disbursed.

**Filter DPD Data:** Use the sidebar to choose the DPD filter value. This value determines the threshold for considering loans in the DPD analysis.

## Example Usage
1. Open the terminal in WSL or Mac.
2. Navigate to the directory containing the script.
3. Run the command to start the web app.
4. Explore the "Loans per Quarter" section to understand the distribution of loans across quarters.
5. Analyze the "DPD per Quarter" section to identify loans with DPD values exceeding the selected threshold in each quarter.

## Additional Notes
- The data is processed and visualized dynamically based on the selected DPD filter value.
- Ensure the data file path is correctly specified for accurate results.
