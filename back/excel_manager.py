from openpyxl import Workbook, worksheet, load_workbook 

def _load_database() -> Workbook:
    return load_workbook("./back/data/companies.xlsx")

def get_companies() -> list[str]:
    wb = _load_database()
    ws = wb.active
    companies = []
    for col in ws.iter_cols(min_col=0, max_col=ws.max_column):
        if col[0].value.lower() in ["domain", "domains"]:
            for row in col[1:]:
                companies.append(row.value)
    
    return companies