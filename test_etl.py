#!/usr/bin/env python3
"""
ETLパイプラインのテストスクリプト
"""

import pandas as pd
import os
from simple_etl import SimpleETL

def test_etl_pipeline():
    """
    ETLパイプラインの基本テスト
    """
    print("=== ETLパイプライン テスト開始 ===")
    
    # ETLインスタンスの作成
    etl = SimpleETL()
    
    # テスト1: サンプルデータでの実行
    print("\n--- テスト1: サンプルデータでの実行 ---")
    success1 = etl.run_pipeline(source_type='sample', output_type='csv')
    
    if success1:
        print("✓ サンプルデータでのテスト成功")
        
        # 結果の確認
        if os.path.exists('output/transformed_employees.csv'):
            df = pd.read_csv('output/transformed_employees.csv')
            print(f"✓ 出力ファイル確認: {len(df)}件のデータ")
            
            # 変換結果の確認
            print("\n変換結果の確認:")
            print(f"- 年齢グループ: {df['age_group'].value_counts().to_dict()}")
            print(f"- 給与レベル: {df['salary_level'].value_counts().to_dict()}")
            print(f"- 部署別: {df['department'].value_counts().to_dict()}")
    else:
        print("✗ サンプルデータでのテスト失敗")
    
    # テスト2: CSVファイルでの実行
    print("\n--- テスト2: CSVファイルでの実行 ---")
    if os.path.exists('sample_data.csv'):
        etl2 = SimpleETL()
        success2 = etl2.run_pipeline(source_type='csv', output_type='json')
        
        if success2:
            print("✓ CSVファイルでのテスト成功")
        else:
            print("✗ CSVファイルでのテスト失敗")
    else:
        print("✗ sample_data.csvが見つかりません")
    
    # テスト3: データベース出力の確認
    print("\n--- テスト3: データベース出力の確認 ---")
    if os.path.exists('output/etl_database.db'):
        import sqlite3
        conn = sqlite3.connect('output/etl_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✓ データベーステーブル: {[table[0] for table in tables]}")
        
        cursor.execute("SELECT COUNT(*) FROM employees;")
        count = cursor.fetchone()[0]
        print(f"✓ データベース内のレコード数: {count}")
        conn.close()
    else:
        print("✗ データベースファイルが見つかりません")

def test_data_validation():
    """
    データ検証テスト
    """
    print("\n=== データ検証テスト ===")
    
    if os.path.exists('output/transformed_employees.csv'):
        df = pd.read_csv('output/transformed_employees.csv')
        
        # 必須カラムの確認
        required_columns = ['id', 'name', 'age', 'department', 'salary', 'age_group', 'salary_level', 'years_of_service']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if not missing_columns:
            print("✓ 必須カラムが全て存在します")
        else:
            print(f"✗ 不足しているカラム: {missing_columns}")
        
        # データ型の確認
        print(f"✓ データ型確認:")
        print(f"  - 年齢: {df['age'].dtype}")
        print(f"  - 給与: {df['salary'].dtype}")
        print(f"  - 勤続年数: {df['years_of_service'].dtype}")
        
        # データ範囲の確認
        print(f"✓ データ範囲確認:")
        print(f"  - 年齢範囲: {df['age'].min()} - {df['age'].max()}")
        print(f"  - 給与範囲: {df['salary'].min():,} - {df['salary'].max():,}")
        print(f"  - 勤続年数範囲: {df['years_of_service'].min():.1f} - {df['years_of_service'].max():.1f}")

if __name__ == "__main__":
    test_etl_pipeline()
    test_data_validation()
    print("\n=== テスト完了 ===") 