import os
import glob
import csv
import subprocess
from typing import List, Dict, Optional

# ==== À MODIFIER SELON TON PC ====
OPENFACE_DIR = r"C:\Users\user\Documents\memoire\openface"
FEATURE_EXE = os.path.join(OPENFACE_DIR, "FeatureExtraction.exe")

IMAGES_DIR = r"C:\Users\user\Documents\memoire\dataset\images_raw"
OUT_DIR = r"C:\Users\user\Documents\memoire\results\openface_batch"
LABELS_OUT = r"C:\Users\user\Documents\memoire\dataset\labels.csv"

# Seuils simples (à ajuster plus tard)
AU6_THR = 1.0
AU12_THR = 1.0


def run_openface_on_dir(images_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    cmd = [
        FEATURE_EXE,
        "-fdir", images_dir,
        "-aus",
        "-out_dir", out_dir
    ]
    print("Running OpenFace:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def find_openface_csv(out_dir: str) -> str:
    csvs = glob.glob(os.path.join(out_dir, "*.csv"))
    if not csvs:
        raise FileNotFoundError(f"Aucun CSV trouvé dans {out_dir}")
    csvs.sort(key=os.path.getmtime, reverse=True)
    return csvs[0]


def _to_float(x: str) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def build_labels(openface_csv: str, labels_out: str):
    with open(openface_csv, "r", newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter=",")
        # Nettoyer les noms de colonnes (supprimer espaces)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]  # type: ignore
        rows: List[Dict[str, str]] = []
        for r in reader:
            rows.append({k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()})

    if not rows:
        raise RuntimeError("CSV OpenFace vide.")

    # Trouver la colonne nom de fichier si présente (selon versions OpenFace)
    filename_col: Optional[str] = None
    for col in ["file", "filename", "image", "file_name", "name"]:
        if col in rows[0]:
            filename_col = col
            break

    out_rows = []
    duchenne_count = 0
    non_count = 0

    for i, r in enumerate(rows):
        # Filtrer si OpenFace indique success=1
        if "success" in r:
            try:
                if int(float(r["success"])) != 1:
                    continue
            except Exception:
                pass

        au6 = _to_float(r.get("AU06_r", "0"))
        au12 = _to_float(r.get("AU12_r", "0"))

        # reconstruire le chemin image si possible
        if filename_col is None:
            image_path = f"unknown_{i}.jpg"
        else:
            val = (r.get(filename_col) or "").strip()
            image_path = val if os.path.isabs(val) else os.path.join(IMAGES_DIR, val)

        label = "duchenne" if (au6 >= AU6_THR and au12 >= AU12_THR) else "non_duchenne"
        if label == "duchenne":
            duchenne_count += 1
        else:
            non_count += 1

        out_rows.append({
            "image_path": image_path,
            "AU06_r": f"{au6:.4f}",
            "AU12_r": f"{au12:.4f}",
            "label": label
        })

    os.makedirs(os.path.dirname(labels_out), exist_ok=True)
    with open(labels_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image_path", "AU06_r", "AU12_r", "label"])
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"✅ Labels écrits dans: {labels_out}")
    print(f"duchenne={duchenne_count} | non_duchenne={non_count} | total={duchenne_count + non_count}")


def main():
    run_openface_on_dir(IMAGES_DIR, OUT_DIR)
    csv_path = find_openface_csv(OUT_DIR)
    print("CSV OpenFace trouvé:", csv_path)
    build_labels(csv_path, LABELS_OUT)


if __name__ == "__main__":
    main()