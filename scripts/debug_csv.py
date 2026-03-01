import csv

CSV_PATH = r"C:\Users\user\Documents\memoire\results\openface_batch\images_raw.csv"

with open(CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
    sample = f.read(2000)

print("=== Aperçu brut (2000 premiers caractères) ===")
print(sample[:500].replace("\n", "\\n\n"))

# tester séparateurs
for delim in ["\t", ",", ";"]:
    with open(CSV_PATH, "r", newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter=delim)
        rows = list(reader)
    print(f"\n=== Test delimiter={repr(delim)} ===")
    if not rows:
        print("Aucune ligne lue")
        continue
    print("Colonnes détectées (10 premières) :", list(rows[0].keys())[:10])
    print("AU06_r lu :", rows[0].get("AU06_r"))
    print("AU12_r lu :", rows[0].get("AU12_r"))
    print("success lu :", rows[0].get("success"))