# ETL トレーニングプロジェクト

個人でETL（Extract, Transform, Load）パイプラインを学習・テストするための簡単なプロジェクトです。

## 概要

このプロジェクトでは、以下のETL処理を実装しています：

- **Extract（抽出）**: サンプルデータまたはCSVファイルからデータを抽出
- **Transform（変換）**: 年齢グループ、給与レベル、勤続年数などの計算
- **Load（読み込み）**: CSV、JSON、SQLiteデータベースに結果を保存

## セットアップ

1. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```

2. ETLパイプラインを実行：
```bash
python simple_etl.py
```

## ファイル構成

- `simple_etl.py`: メインのETLパイプライン
- `sample_data.csv`: サンプルデータ
- `requirements.txt`: 必要なPythonパッケージ
- `output/`: 処理結果の出力ディレクトリ

## 出力ファイル

実行後、以下のファイルが生成されます：

- `output/transformed_employees.csv`: 変換後のデータ（CSV形式）
- `output/transformed_employees.json`: 変換後のデータ（JSON形式）
- `output/etl_database.db`: SQLiteデータベース

## 変換処理の内容

1. **年齢グループの追加**: 20代、30代、40代以上に分類
2. **給与レベルの追加**: 低、中、高に分類
3. **勤続年数の計算**: 入社日から現在までの年数
4. **部署別統計**: 部署ごとの平均給与、人数、平均年齢

## カスタマイズ

`simple_etl.py`の`SimpleETL`クラスを拡張することで、独自の変換処理を追加できます。
