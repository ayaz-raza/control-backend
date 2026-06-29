import pandas as pd

df = pd.read_excel("data/Master_Sheet.xlsx")

df.columns = df.columns.str.strip()

def get_pcode_details(pcode):

    result = df[
        df["P-Code"].astype(str).str.upper()
        == pcode.upper()
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "project_code": str(row["Project Code"]),
        "system": str(row["System"]),
        "pcode": str(row["P-Code"]),
        "ftb": str(row["FTB"]),
        "description": str(row["Description"]),
        "causes": str(row["Causes"]),
        "vehicle_reaction": str(row["Vehicle Reaction"]),
        "remedies": str(row["Remedies"])
    }

def get_ftb_list(pcode):

    result = df[
        df["P-Code"].astype(str).str.upper()
        == pcode.upper()
    ]

    if result.empty:
        return []

    return sorted(
        result["FTB"].astype(str).unique().tolist()
    )

def get_pcode_ftb_details(pcode, ftb):

    result = df[
        (df["P-Code"].astype(str).str.upper() == pcode.upper()) &
        (df["FTB"].astype(str).str.upper() == ftb.upper())
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "project_code": str(row["Project Code"]),
        "system": str(row["System"]),
        "pcode": str(row["P-Code"]),
        "ftb": str(row["FTB"]),
        "description": str(row["Description"]),
        "causes": str(row["Causes"]),
        "vehicle_reaction": str(row["Vehicle Reaction"]),
        "remedies": str(row["Remedies"])
    }