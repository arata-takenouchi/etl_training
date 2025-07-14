#!/usr/bin/env python3
"""
簡単なETLパイプラインの例
個人でのテスト用
"""

import pandas as pd
import json
import sqlite3
from datetime import datetime
import os

class SimpleETL:
    def __init__(self):
        self.extracted_data = None
        self.transformed_data = None
        
    def extract(self, source_type='sample'):
        """
        データの抽出（Extract）
        """
        print("データを抽出中...")
        
        if source_type == 'sample':
            # サンプルデータを作成
            data = {
                'id': [1, 2, 3, 4, 5],
                'name': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲', '伊藤健太'],
                'age': [25, 30, 35, 28, 32],
                'department': ['営業部', '開発部', '営業部', '人事部', '開発部'],
                'salary': [300000, 450000, 350000, 380000, 500000],
                'join_date': ['2020-01-15', '2018-03-20', '2019-07-10', '2021-02-28', '2017-11-05']
            }
            self.extracted_data = pd.DataFrame(data)
            
        elif source_type == 'csv':
            # CSVファイルから読み込み
            if os.path.exists('sample_data.csv'):
                self.extracted_data = pd.read_csv('sample_data.csv')
            else:
                print("CSVファイルが見つかりません")
                return False
                
        print(f"抽出完了: {len(self.extracted_data)}件のデータ")
        return True
    
    def transform(self):
        """
        データの変換（Transform）
        """
        print("データを変換中...")
        
        if self.extracted_data is None:
            print("抽出データがありません")
            return False
            
        # データの変換処理
        df = self.extracted_data.copy()
        
        # 1. 年齢グループの追加
        df['age_group'] = df['age'].apply(lambda x: 
            '20代' if x < 30 else '30代' if x < 40 else '40代以上')
        
        # 2. 給与レベルの追加
        df['salary_level'] = df['salary'].apply(lambda x: 
            '低' if x < 350000 else '中' if x < 450000 else '高')
        
        # 3. 勤続年数の計算
        df['join_date'] = pd.to_datetime(df['join_date'])
        current_date = pd.Timestamp.now()
        df['years_of_service'] = ((current_date - df['join_date']).dt.days / 365).round(1)
        
        # 4. 部署別の統計情報
        dept_stats = df.groupby('department').agg({
            'salary': ['mean', 'count'],
            'age': 'mean'
        }).round(0)
        
        self.transformed_data = {
            'employee_data': df,
            'department_stats': dept_stats
        }
        
        print("変換完了")
        return True
    
    def load(self, output_type='all'):
        """
        データの読み込み（Load）
        """
        print("データを保存中...")
        
        if self.transformed_data is None:
            print("変換データがありません")
            return False
        
        # 結果ディレクトリの作成
        os.makedirs('output', exist_ok=True)
        
        if output_type in ['csv', 'all']:
            # CSVファイルとして保存
            self.transformed_data['employee_data'].to_csv(
                'output/transformed_employees.csv', 
                index=False, 
                encoding='utf-8-sig'
            )
            print("CSVファイルに保存完了: output/transformed_employees.csv")
        
        if output_type in ['json', 'all']:
            # JSONファイルとして保存
            df_for_json = self.transformed_data['employee_data'].copy()
            # Timestampを文字列に変換
            df_for_json['join_date'] = df_for_json['join_date'].dt.strftime('%Y-%m-%d')
            employee_json = df_for_json.to_dict('records')
            with open('output/transformed_employees.json', 'w', encoding='utf-8') as f:
                json.dump(employee_json, f, ensure_ascii=False, indent=2)
            print("JSONファイルに保存完了: output/transformed_employees.json")
        
        if output_type in ['sqlite', 'all']:
            # SQLiteデータベースに保存
            conn = sqlite3.connect('output/etl_database.db')
            self.transformed_data['employee_data'].to_sql(
                'employees', 
                conn, 
                if_exists='replace', 
                index=False
            )
            conn.close()
            print("SQLiteデータベースに保存完了: output/etl_database.db")
        
        return True
    
    def run_pipeline(self, source_type='sample', output_type='all'):
        """
        完全なETLパイプラインを実行
        """
        print("=== ETLパイプライン開始 ===")
        
        # Extract
        if not self.extract(source_type):
            return False
        
        # Transform
        if not self.transform():
            return False
        
        # Load
        if not self.load(output_type):
            return False
        
        print("=== ETLパイプライン完了 ===")
        return True

def main():
    """
    メイン実行関数
    """
    etl = SimpleETL()
    
    # パイプラインを実行
    success = etl.run_pipeline()
    
    if success:
        print("\n=== 結果サマリー ===")
        print(f"処理件数: {len(etl.transformed_data['employee_data'])}件")
        print("\n部署別統計:")
        print(etl.transformed_data['department_stats'])
        
        print("\n出力ファイル:")
        print("- output/transformed_employees.csv")
        print("- output/transformed_employees.json")
        print("- output/etl_database.db")

if __name__ == "__main__":
    main() 