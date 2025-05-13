# Java Method Mapper

このツールは、指定されたクラス一覧CSVとクラス名・物理パスCSVをもとに、対象クラスのすべてのJavaメソッド名を抽出し、`class,method`形式のCSVを出力します。

## 必要ファイル
- クラス名・物理パスCSV（例: class_index.csv）
  - `class_name`, `file_path` カラム必須
- 処理対象クラスCSV（例: target_classes.csv）
  - `RPC_NAME`, `RPC_CLASS` カラム必須

## 使い方
```sh
python main.py class_index.csv target_classes.csv
```

## 出力
- `class,method`カラムのCSV（output_methods.csv）

## 依存ライブラリ
- javalang

### インストール方法（コマンドプロンプトで実行）
```cmd
pip install -r requirements.txt
```

---

## バージョン管理は version_log.md を参照してください。
