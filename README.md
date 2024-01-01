## Progress Report
Done:
- WebApp development complete.
- User Guide created

Work Due:
- Develop and Run test cases
- Fix logical inaccuracies if any.

Points of contention:
- Please check out the logic for calculating the ending DPD per user per quarter.

# Buro BD DPD-Dashboard User Guide

## Introduction
Welcome to the Buro BD DPD-Dashboard! This web application provides insights into the Disbursement and Due Performance Data (DPD) for loans. Use this guide to navigate through the features and functionalities of the dashboard.

## Getting Started
1. **Access the Dashboard:**
    - **WSL (Windows Subsystem for Linux):**
        ```bash
        streamlit run path/to/your/app/dpd_dashboard.py
        ```
    - **Mac/Linux:**
        ```bash
        streamlit run path/to/your/app/dpd_dashboard.py
        ```
2. **Select DPD Filter Value:** On the sidebar, choose the DPD filter value from the radio buttons. You can select from 7, 15, 30, 60, or 90 days.

## Dashboard Sections

### Loans per Quarter
- **Description:** This section provides the number of loans disbursed in each quarter of the fiscal year.
- **Visualization:** A table with columns representing quarters (Q1 to Q4) and rows indicating the number of loans disbursed.

### DPD per Quarter
- **Description:** This section displays the count of loans with DPD values exceeding the selected filter value in each quarter.
- **Visualization:** A table with columns representing quarters (Q1 to Q4) and rows indicating the count of loans with DPD values above the selected threshold.

## Using the Dashboard
1. **Read the Data:** The data is loaded from the "DPD_Sample.xlsx" file. To use a different file, modify the file path in the script.
    - Example:
        ```python
        df = pd.read_excel("path/to/your/data/file.xlsx")
        ```

2. **Understand Disbursement and Due Quarters:**
   - Disbursement Quarter: Represents the quarter in which the loan was disbursed.
   - Due Quarter: Represents the quarter in which the payment is due.

3. **Interpret DPD Values:**
   - DPD (Days Past Due): Indicates the number of days a payment is overdue.

4. **Filter DPD Data:**
   - Use the sidebar to choose the DPD filter value. This value determines the threshold for considering loans in the DPD analysis.

## Example Usage
1. Open the terminal in WSL or Mac.
2. Navigate to the directory containing the script.
3. Run the command to start the web app.
4. Explore the "Loans per Quarter" section to understand the distribution of loans across quarters.
5. Analyze the "DPD per Quarter" section to identify loans with DPD values exceeding the selected threshold in each quarter.

## Additional Notes
- The data is processed and visualized dynamically based on the selected DPD filter value.
- Ensure the data file path is correctly specified for accurate results.

Thank you for using the Buro BD DPD-Dashboard!

