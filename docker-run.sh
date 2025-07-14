#!/bin/bash

# ETL Docker環境の管理スクリプト

set -e

# 色付きの出力関数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# ヘルプ表示
show_help() {
    echo "ETL Docker環境管理スクリプト"
    echo ""
    echo "使用方法:"
    echo "  $0 build     - Dockerイメージをビルド"
    echo "  $0 run       - ETLパイプラインを実行"
    echo "  $0 test      - ETLテストを実行"
    echo "  $0 shell     - コンテナ内でシェルを起動"
    echo "  $0 clean     - コンテナとイメージを削除"
    echo "  $0 logs      - ログを表示"
    echo "  $0 help      - このヘルプを表示"
    echo ""
}

# Dockerイメージのビルド
build_image() {
    print_info "Dockerイメージをビルド中..."
    docker-compose build
    print_success "ビルド完了"
}

# ETLパイプラインの実行
run_etl() {
    print_info "ETLパイプラインを実行中..."
    docker-compose run --rm etl-app
    print_success "ETLパイプライン実行完了"
}

# ETLテストの実行
run_test() {
    print_info "ETLテストを実行中..."
    docker-compose run --rm etl-test
    print_success "ETLテスト実行完了"
}

# コンテナ内でシェルを起動
run_shell() {
    print_info "コンテナ内でシェルを起動中..."
    docker-compose run --rm etl-app /bin/bash
}

# クリーンアップ
clean_up() {
    print_info "コンテナとイメージを削除中..."
    docker-compose down --rmi all --volumes --remove-orphans
    print_success "クリーンアップ完了"
}

# ログ表示
show_logs() {
    print_info "ログを表示中..."
    docker-compose logs
}

# メイン処理
case "${1:-help}" in
    "build")
        build_image
        ;;
    "run")
        run_etl
        ;;
    "test")
        run_test
        ;;
    "shell")
        run_shell
        ;;
    "clean")
        clean_up
        ;;
    "logs")
        show_logs
        ;;
    "help"|*)
        show_help
        ;;
esac 