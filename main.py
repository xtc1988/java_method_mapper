import csv
import sys
import os
import javalang
from pathlib import Path

def read_class_index(csv_path):
    """class_name, file_path の辞書を返す"""
    mapping = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row['class_name']] = row['file_path']
    return mapping

def read_target_classes(csv_path):
    """RPC_CLASSのリストを返す"""
    targets = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            targets.append(row['RPC_CLASS'])
    return targets

def extract_methods(java_path):
    """Javaファイルから全メソッド名を抽出"""
    methods = set()
    try:
        with open(java_path, encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
        for path, node in tree:
            if isinstance(node, javalang.tree.MethodDeclaration):
                methods.add(node.name)
    except Exception as e:
        print(f"[WARN] {java_path} の解析中にエラー: {e}")
    return list(methods)

def main():
    if len(sys.argv) < 3:
        print('Usage: python main.py <class_index.csv> <target_classes.csv>')
        sys.exit(1)
    class_index_csv = sys.argv[1]
    target_classes_csv = sys.argv[2]
    output_csv = 'output_methods.csv'

    class_map = read_class_index(class_index_csv)
    targets = read_target_classes(target_classes_csv)

    results = []
    for class_name in targets:
        java_path = class_map.get(class_name)
        if java_path and os.path.exists(java_path):
            methods = extract_methods(java_path)
            for m in methods:
                results.append({'class': class_name, 'method': m})
        else:
            print(f"[WARN] {class_name} のJavaファイルが見つかりません")

    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['class', 'method'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"{len(results)}件のメソッドを{output_csv}に出力しました")

if __name__ == '__main__':
    main()
