# ETL トレーニングプロジェクト

個人でETL（Extract, Transform, Load）パイプラインを学習・テストするための簡単なプロジェクトです。

## 概要

このプロジェクトでは、以下のETL処理を実装しています：

- **Extract（抽出）**: サンプルデータまたはCSVファイルからデータを抽出
- **Transform（変換）**: 年齢グループ、給与レベル、勤続年数などの計算
- **Load（読み込み）**: CSV、JSON、SQLiteデータベースに結果を保存

## セットアップ

### 方法1: ローカル環境（仮想環境）

1. 必要なパッケージをインストール：
```bash
python3 -m venv etl_env
source etl_env/bin/activate
pip install -r requirements.txt
```

2. ETLパイプラインを実行：
```bash
python simple_etl.py
```

### 方法2: Docker環境（推奨）

PC本体に影響を与えないDocker環境で実行できます。

#### 前提条件
- Docker Desktop がインストールされていること

#### 使用方法

1. **Dockerイメージをビルド**：
```bash
./docker-run.sh build
```

2. **ETLパイプラインを実行**：
```bash
./docker-run.sh run
```

3. **ETLテストを実行**：
```bash
./docker-run.sh test
```

4. **コンテナ内でシェルを起動**（デバッグ用）：
```bash
./docker-run.sh shell
```

5. **クリーンアップ**：
```bash
./docker-run.sh clean
```

#### 便利なコマンド

```bash
# ヘルプ表示
./docker-run.sh help

# ログ表示
./docker-run.sh logs

# 直接Docker Composeを使用
docker-compose up etl-app    # ETLパイプライン実行
docker-compose up etl-test   # テスト実行
```

## ファイル構成

- `simple_etl.py`: メインのETLパイプライン
- `sample_data.csv`: サンプルデータ
- `requirements.txt`: 必要なPythonパッケージ
- `Dockerfile`: Docker環境の定義
- `docker-compose.yml`: Docker Compose設定
- `docker-run.sh`: Docker環境管理スクリプト
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
