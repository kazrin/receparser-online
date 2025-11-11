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
pip install -e .
```

または、直接依存関係をインストール：

```bash
pip install streamlit pandas
```

## 使い方

### アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます。

### レセプトファイルの可視化

1. 左側のサイドバーからレセプトファイル（CSV形式、Shift-JISエンコーディング）をアップロード
2. レセプトタイプ（DPCまたは医科）を選択
3. カルテ番号を選択
4. レコードタイプ（RE, HO, SBなど）を選択
5. データをテーブル形式で確認し、必要に応じてCSVとしてダウンロード

## 対応レコードタイプ

- **RE**: レセプト共通レコード
- **HO**: 公費レコード
- **SB**: 傷病名レコード
- **KO**: コメントレコード
- その他、レセプトファイルに含まれるすべてのレコードタイプ

## 参考情報

- [receparser GitHub](https://github.com/stagira13/receparser)
- [レセプト仕様一覧](https://shinryohoshu.mhlw.go.jp/shinryohoshu/receMenu/doReceInfo)

