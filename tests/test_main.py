import os
import csv
import shutil
import sys
import subprocess

def setup_test_env():
    # テスト用ディレクトリ・ファイル作成
    os.makedirs('tests/tmp', exist_ok=True)
    # サンプルJava
    java_code = '''
    package com.example;
    public class SampleClass {
        public void methodA() {}
        public int methodB(int x) { return x; }
        private void hidden() {}
    }
    '''
    with open('tests/tmp/SampleClass.java', 'w', encoding='utf-8') as f:
        f.write(java_code)
    # class_index.csv
    with open('tests/tmp/class_index.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['class_name', 'file_path'])
        writer.writerow(['com.example.SampleClass', os.path.abspath('tests/tmp/SampleClass.java')])
    # target_classes.csv
    with open('tests/tmp/target_classes.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['RPC_NAME', 'RPC_CLASS'])
        writer.writerow(['SAMPLE', 'com.example.SampleClass'])

def teardown_test_env():
    shutil.rmtree('tests/tmp', ignore_errors=True)

def test_method_extraction():
    setup_test_env()
    try:
        # main.pyを実行
        result = subprocess.run([
            sys.executable, 'main.py',
            'tests/tmp/class_index.csv',
            'tests/tmp/target_classes.csv'
        ], capture_output=True, text=True)
        assert result.returncode == 0
        # 出力CSV確認
        with open('output_methods.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        method_names = set(r['method'] for r in rows)
        assert 'methodA' in method_names
        assert 'methodB' in method_names
        # privateメソッドも含まれる（仕様通り）
        assert 'hidden' in method_names
        print('テスト成功')
    finally:
        teardown_test_env()

if __name__ == '__main__':
    test_method_extraction()
