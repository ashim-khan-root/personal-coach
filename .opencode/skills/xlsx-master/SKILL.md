---
name: xlsx-master
description: When the user wants to create, edit, analyze, or work with Excel/CSV spreadsheets. Also use when the user mentions "Excel," "spreadsheet," "CSV," "XLSX", "data analysis," "pivot table," "chart from data," "financial model," "product catalog," "inventory spreadsheet," "product data," or "export to Excel." Use this whenever someone needs to work with spreadsheet data — from creating product catalogs to financial analysis. For data visualization, see d3-visualization.
metadata:
  version: 1.0.0
---

# XLSX Master

You are a spreadsheet expert. Your goal is to create, edit, and analyze Excel/CSV files with professional formatting and useful formulas.

## Before Working

Gather this context:

### 1. Data Source
- What data do you have? (CSV, database, manual input)
- How many rows/columns?
- What format is it in?

### 2. Purpose
- What will this spreadsheet be used for?
- Who will use it?
- What decisions will it inform?

### 3. Requirements
- Specific columns needed?
- Formulas required?
- Formatting preferences?
- Charts needed?

---

## File Formats

| Format | Use Case | Limitations |
|--------|----------|-------------|
| `.xlsx` | Full Excel features, formatting, formulas | Microsoft ecosystem |
| `.csv` | Simple data exchange, universal | No formulas, no formatting |
| `.xls` | Legacy Excel | Deprecated, avoid |
| `.tsv` | Tab-separated values | Niche use cases |

---

## Spreadsheet Patterns

### Product Catalog
```csv
SKU,Name,Category,Price,Cost,Margin,Stock,Status
SEC-001,Smart Lock Pro,Access Control,499,280,44%,45,Active
SEC-002,4K Camera System,Surveillance,899,520,42%,23,Active
SEC-003,Video Doorbell,Smart Home,299,150,50%,67,Active
```

### Financial Model
```csv
Category,Jan,Feb,Mar,Q1 Total,% of Revenue
Revenue,45000,52000,48000,145000,100%
COGS,18000,20800,19200,58000,40%
Gross Profit,27000,31200,28800,87000,60%
Operating Expenses,15000,15000,15000,45000,31%
Net Profit,12000,16200,13800,42000,29%
```

### Project Tracker
```csv
Task,Owner,Status,Priority,Start Date,Due Date,Progress
SEO Audit,Hamid,In Progress,High,2026-05-01,2026-05-15,75%
Blog Content,Sarah,Not Started,Medium,2026-05-10,2026-05-30,0%
Facebook Setup,Hamid,In Progress,High,2026-05-20,2026-06-01,40%
```

---

## Common Formulas

### Basic
```excel
=SUM(A1:A10)           # Sum range
=AVERAGE(B1:B10)       # Average
=COUNT(A1:A10)         # Count numbers
=MAX(C1:C10)           # Maximum
=MIN(D1:D10)           # Minimum
```

### Conditional
```excel
=IF(A1>100,"High","Low")                    # Conditional
=COUNTIF(A:A,"Active")                       # Count with condition
=SUMIF(B:B,">100",C:C)                       # Sum with condition
=AVERAGEIF(A:A,"Sales",B:B)                  # Average with condition
```

### Lookup
```excel
=VLOOKUP(A1,Table1,2,FALSE)                 # Vertical lookup
=INDEX(B:B,MATCH(A1,A:A,0))                 # Index-match
=XLOOKUP(A1,A:A,B:B,"Not found")            # Modern lookup
```

### Text
```excel
=LEFT(A1,5)                                  # First 5 chars
=RIGHT(A1,3)                                 # Last 3 chars
=MID(A1,2,4)                                 # Extract from middle
=LEN(A1)                                     # Length
=UPPER(A1)                                   # Uppercase
=LOWER(A1)                                   # Lowercase
=TRIM(A1)                                    # Remove spaces
=CONCATENATE(A1," ",B1)                      # Join text
```

### Date
```excel
=TODAY()                                     # Current date
=NOW()                                       # Current date/time
=DATEDIF(A1,B1,"D")                          # Days between
=EDATE(A1,3)                                 # 3 months later
=YEAR(A1)                                    # Extract year
=MONTH(A1)                                   # Extract month
```

### Financial
```excel
=PMT(0.05/12,60,10000)                       # Loan payment
=FV(0.05,10,-1000,0)                         # Future value
=NPV(0.1,A1:A10)                             # Net present value
=IRR(A1:A10)                                 # Internal rate of return
```

---

## Data Analysis Patterns

### Pivot Table Summary
```
Rows: Category
Values: SUM of Revenue, COUNT of Orders, AVERAGE of Rating
Filter: Date Range, Region
```

### Running Total
```excel
=SUM($C$2:C2)  # Copy down for running total
```

### Percent Change
```excel
=(B2-A2)/A2  # Format as percentage
```

### Year-over-Year
```excel
=(B13-B1)/B1  # Compare same month last year
```

---

## Formatting Best Practices

### Headers
- Bold, centered
- Background color (light gray or brand color)
- Freeze top row

### Numbers
- Currency: `$#,##0.00`
- Percentage: `0.0%`
- Large numbers: `#,##0` (with comma separator)

### Conditional Formatting
```excel
# Highlight cells
=IF(A1>100, "Green", IF(A1>50, "Yellow", "Red"))

# Data bars (Excel feature)
Home → Conditional Formatting → Data Bars
```

### Column Width
- Auto-fit to content
- Minimum 12 characters for readability
- Maximum 50 characters before wrapping

---

## CSV Generation (Python)

```python
import csv

data = [
    ["SKU", "Name", "Price", "Stock"],
    ["SEC-001", "Smart Lock", 499, 45],
    ["SEC-002", "4K Camera", 899, 23],
]

with open("catalog.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

---

## Output

When creating spreadsheets:
1. Provide complete data (not truncated)
2. Include headers with clear labels
3. Add formulas where useful
4. Format numbers appropriately
5. Include data validation where applicable
6. Provide both CSV and formatted Excel versions
