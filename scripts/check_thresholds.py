import csv

LABELS_IN = r"C:\Users\user\Documents\memoire\results\openface_batch\images_raw.csv"

rows = []
with open(LABELS_IN, "r", newline="", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if "success" in r:
            try:
                if int(float(r["success"])) != 1:
                    continue
            except Exception:
                pass
        def to_float(x):
            try: return float(x)
            except: return 0.0
        au6 = to_float(r.get("AU06_r", "0"))
        au12 = to_float(r.get("AU12_r", "0"))
        rows.append((au6, au12, r.get("filename", r.get("file", ""))))

rows.sort(reverse=True, key=lambda x: x[0])

print("Top 10 AU06_r:")
for au6, au12, name in rows[:10]:
    print(f"AU06_r={au6:.2f} | AU12_r={au12:.2f} | {name}")

rows.sort(reverse=True, key=lambda x: x[1])
print("\nTop 10 AU12_r:")
for au6, au12, name in rows[:10]:
    print(f"AU06_r={au6:.2f} | AU12_r={au12:.2f} | {name}")