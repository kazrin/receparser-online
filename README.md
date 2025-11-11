# Receparser Online

電子レセプトファイルをブラウザ上で可視化するStreamlitアプリケーションです。

## 機能

- レセプトファイル（CSV形式、Shift-JISエンコーディング）のアップロード
- DPCレセプト・医科レセプトの両方に対応
- カルテ番号ごとのレセプトデータの表示
- レコードタイプ（RE, HO, SBなど）ごとのデータ可視化
- pandas DataFrame形式でのデータ表示
- CSV形式でのデータダウンロード

## セットアップ

### 依存関係のインストール

```bash
uv pip install -e .
```

## 使い方

### アプリケーションの起動

```bash
uv run streamlit run app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます。

### レセプトファイルの可視化

1. 左側のサイドバーからレセプトファイル（CSV形式、Shift-JISエンコーディング）をアップロード
2. レセプトタイプ（医科またはDCP）を選択

## 使用ライブラリ

このプロジェクトは以下のライブラリを使用しています：

- **[receparser](https://github.com/stagira13/receparser)** - 電子レセプトファイルを読み込むためのパーサライブラリ
  - ライセンス: MIT License
  - 著作権: Copyright (c) 2018 Stagira
  - 使用バージョン: [334246e](https://github.com/stagira13/receparser/commit/334246efd4c3d5b14b566096b39476c16863b719) (commit: `334246efd4c3d5b14b566096b39476c16863b719`)

receparserはプロジェクト内の`receparser/`ディレクトリから直接読み込まれます。
streamlitにアプリをデプロイするため、submoduleではなく、ディレクトリ/ファイルとして配置しています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

### サードパーティライブラリのライセンス

#### receparser

ライセンス全文は [`receparser/LICENSE.txt`](receparser/LICENSE.txt) を参照してください。

## 参考情報

- [receparser GitHub](https://github.com/stagira13/receparser)
- [レセプト仕様一覧](https://shinryohoshu.mhlw.go.jp/shinryohoshu/receMenu/doReceInfo)

