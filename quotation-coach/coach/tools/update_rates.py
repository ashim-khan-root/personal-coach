"""Update rates from Excel file. Wrapper around make_quotation.py --update-rates.
Usage: python update_rates.py <file.xlsx>
"""
import sys
from make_quotation import update_rates_from_excel

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_rates.py <path_to_excel.xlsx>")
        sys.exit(1)
    update_rates_from_excel(sys.argv[1])

if __name__ == "__main__":
    main()
