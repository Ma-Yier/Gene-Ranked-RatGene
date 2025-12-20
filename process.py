import os
import glob

def extract_prefix_before_colon(line: str) -> str:
    s = line.strip()
    idx_cn = s.find('：')
    idx_en = s.find(':')
    idxs = [i for i in [idx_cn, idx_en] if i != -1]
    if idxs:
        cut = min(idxs)
        return s[:cut].strip()
    else:
        return None 

def read_txt_and_extract(path: str):
    results = []
    with open(path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            append_line = extract_prefix_before_colon(line)
            if append_line == 'total grRules':
                continue
            results.append(append_line)
    return results

def save_matlab_readable(base_name: str, data_list):
        if not os.path.exists("CSV"):
            os.mkdir("CSV")
        csv_path = f"CSV/{base_name}.csv"
        try:
            import csv
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for item in data_list:
                    writer.writerow([item])
            print(f"[OK] save CSV: {csv_path}")
            print("NOTE: MATLAB call fucntion readtable or textscan to read CSV.")
        except Exception as e2:
            print(f"[ERR] failed to save: {e2}")

def main():
    txt_files = glob.glob("*.txt")
    if not txt_files:
        print("no .txt in current filefolder.")
        return

    print(f"detect {len(txt_files)}  .txt files:")
    for p in txt_files:
        print(" -", p)

    for txt_path in txt_files:
        base_name = os.path.splitext(os.path.basename(txt_path))[0]
        data_list = read_txt_and_extract(txt_path)
        print(f"\nfile: {txt_path}(name: {base_name})")
        print(f"exract {len(data_list)} logs. example(top 5):")
        for item in data_list[:5]:
            print("   >", item)
        save_matlab_readable(base_name, data_list)

if __name__ == "__main__":
    main()