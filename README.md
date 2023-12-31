# BURO BD DPD-Dashboard

## Progress Report
Done:
- WebApp development complete.
- User Guide created

Work Due:
- Develop and Run test cases

## Overview

The BURO BD DPD-Dashboard s a visual analysis of loans based on disbursement and due quarters, as well as the Days Past Due (DPD) metric. Users can interact with the app to explore the number of loans and DPD trends across different quarters.

## How to Use

1. **Accessing the Web App:**
   - Make sure you have Streamlit installed. If not, install it using `pip install streamlit`.
   - Save the provided code in a Python file, e.g., `dpd_dashboard.py`.
   - Open a terminal and navigate to the directory containing the file.
   - Run the app using the command: `streamlit run dpd_dashboard.py`.

2. **Web App Interface:**
   - The app opens in your default web browser, displaying the title "Loan Analysis Web App" and a selection panel.

3. **Selecting DPD Filter:**
   - In the selection panel, you will find a radio button group labeled "Select DPD Filter." This allows you to choose predefined DPD filter values:
     - "7+ DPD": Loans with 7 or more days past due.
     - "30+ DPD": Loans with 30 or more days past due.
     - "60+ DPD": Loans with 60 or more days past due.

4. **Viewing Results:**
   - After selecting a DPD filter, the app automatically updates and displays a visual DataFrame. The DataFrame shows the number of loans for each quarter (Q1, Q2, Q3, Q4) based on the chosen DPD filter.

5. **Submit Button:**
   - Below the DPD filter options, you'll find a "Submit" button. Clicking this button triggers the calculation and visualization of loan data based on the selected DPD filter.

6. **Exiting the App:**
   - To exit the app, simply close the web browser or terminate the Streamlit process in the terminal.

## Notes

- Ensure that the necessary Python libraries (`streamlit` and `pandas`) are installed before running the app.
- The app reads data from an Excel file named "DPD_Sample.xlsx." Make sure this file is present in the same directory as the app file. Or change the source code to contain the appropriate file path.
- The app performs calculations based on the loan disbursement and due quarters, as well as the DPD metric, providing valuable insights into loan trends.
