# HR Analytics: Employee Retention & Workforce Insights

## Project Overview
This project focuses on identifying key drivers of employee attrition using exploratory data analysis (EDA) and dynamic business intelligence reporting. By evaluating structural metrics such as department, monthly compensation, job tenure, and work hours, this dashboard uncovers actionable retention risk factors to optimize organizational talent management.

## Core Business KPIs
* **Total Headcount:** 1.47K active employee records analyzed.
* **Average Compensation:** \$6.50K median monthly salary base.
* **Baseline Attrition Rate:** 16.09% overall turnover (exceeding standard 10% healthy enterprise thresholds).

---

## Key Business Questions Answered

### 1. Which business departments are most vulnerable to talent loss?
* **Finding:** While the **Research & Development** department handles the highest raw *volume* of employee exits due to its massive headcount, the **Sales** department demonstrates a significantly higher *proportional* turnover rate relative to its total size, marking it a critical operational risk area.

### 2. Does mandatory overtime directly impact employee flight risk?
* **Finding:** Yes, definitively. The attrition segment among employees who log regular **Overtime** is nearly **double** the size of the turnover segment among those who do not. Burnout is a primary structural catalyst for employee departures in this workforce.

### 3. What are the salary and tenure profiles of departing employees?
* **Finding:** Turnover is heavily concentrated in the bottom-left quadrant of the workforce lifecycle. Employees with **low tenure (0 to 5 years)** earning **lower monthly salaries (\$2K to \$5K)** represent the vast majority of company exits. Once an employee reaches a 10-year milestone or scales past \$10K/month, retention stabilizes completely.

---

## Tech Stack & Visual Assets
* **Data Processing & EDA:** Python (Pandas, Jupyter Notebooks)
* **BI Architecture:** Power BI Desktop (DAX Measures, Tile Filters, Grid Card UI Layout)
* **Dashboard Preview:**
  ![HR Analytics Dashboard](dashboards/Screenshot%202026-06-27%20165447.png)