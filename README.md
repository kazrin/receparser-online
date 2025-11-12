# Receparser Online Desktop App

電子レセプトファイルを可視化するStreamlitデスクトップアプリケーションです。

## 機能

- レセプトファイル（CSV形式、Shift-JISエンコーディング）のアップロード
- DPCレセプト・医科レセプトの両方に対応
- カルテ番号ごとのレセプトデータの表示
- レコードタイプ（RE, HO, SBなど）ごとのデータ可視化
- pandas DataFrame形式でのデータ表示
- CSV形式でのデータダウンロード
- JSON/Markdown形式でのエクスポート

## クイックスタート

```bash
# 依存関係のインストール
npm install

# Streamlitアプリのビルド
npm run dump streamlit_app

# プレビュー（開発モード）
npm run serve

# デスクトップアプリの配布用パッケージ作成（Mac）
npm run dist -- --mac
```

## セットアップ

### 必要な環境

- Node.js (v16以上)
- npm

### 依存関係のインストール

```bash
npm install
```

## ビルドと実行

### 1. Streamlitアプリのビルド

Streamlitアプリをデスクトップアプリ用にビルドします：

```bash
npm run dump streamlit_app
```

このコマンドは以下を実行します：
- `streamlit_app`ディレクトリを`build/streamlit_app`にコピー
- Pyodideランタイムと必要なパッケージをダウンロード
- Electronアプリのビルドファイルを準備

### 2. プレビュー（開発モード）

ビルドしたアプリをプレビューします：

```bash
npm run serve
```

Electronウィンドウが開き、アプリが表示されます。

### 3. デスクトップアプリの配布用パッケージ作成

#### Mac用

```bash
npm run dist -- --mac
```

#### Windows用

```bash
npm run dist -- --win
```

#### Linux用

```bash
npm run dist -- --linux
```

ビルドされたアプリは`dist/`ディレクトリに出力されます。

## 使い方

1. **アプリを起動**
   - ビルドしたアプリ（`.app`、`.exe`、`.dmg`など）を起動します

2. **レセプトファイルをアップロード**
   - 左側のサイドバーからレセプトファイル（CSV形式、Shift-JISエンコーディング）をアップロードします

3. **レセプトタイプを選択**
   - DPCレセプトまたは医科レセプトを選択します

4. **患者を検索・選択**
   - 検索ボックスで氏名、カタカナ氏名、カルテ番号、レセプト番号で検索できます
   - 検索結果から表示したいレセプトを選択します

5. **データを確認・ダウンロード**
   - レコードタイプごとにデータが表示されます
   - 各レコードタイプをCSVとしてダウンロードできます
   - 全レコードをJSONまたはMarkdown形式でエクスポートできます

## プロジェクト構造

```
receparser-online/
├── streamlit_app/          # Streamlitアプリケーション
│   ├── streamlit_app.py    # メインアプリケーション
│   └── receparser/         # receparserライブラリ
│       └── receparser/
│           ├── core.py     # コア機能
│           ├── codes/      # レコードコード定義
│           └── utils.py    # ユーティリティ関数
├── build/                  # ビルドアーティファクト（自動生成）
├── dist/                   # 配布用パッケージ（自動生成）
├── package.json            # Node.js依存関係
├── requirements.txt        # Python依存関係
└── README.md              # このファイル
```

## 技術スタック

- **Streamlit**: Webアプリケーションフレームワーク
- **@stlite/desktop**: Streamlitをデスクトップアプリ化
- **Electron**: デスクトップアプリフレームワーク
- **Pyodide**: ブラウザでPythonを実行
- **receparser**: 電子レセプトファイルパーサーライブラリ

## 注意事項

- レセプトファイルはShift-JISエンコーディングのCSV形式である必要があります
- 大きなファイルの処理には時間がかかる場合があります
- アップロードされたファイルは一時的に保存されますが、アプリ終了時に削除されます
- `japanera`パッケージはPyodideで利用可能な場合のみインストールされます。利用できない場合は、元号変換機能が制限される可能性があります
- `receparser`ライブラリは`streamlit_app/receparser`配下に直接配置されており、デスクトップアプリ環境で自動的にインポートされます

## カスタマイズ

### アプリ名とアイコンの変更

Macアプリの名前とアイコンを変更するには：

1. **アプリ名の変更**
   - `package.json`の`build.productName`を変更します
   - 例: `"productName": "Receparser Online"`

2. **アイコンの変更**
   - Mac用のアイコンファイル（`.icns`形式）を準備します
   - アイコンファイルを`assets/icon.icns`に配置します
   - `.icns`ファイルの作成方法：
     - 1024x1024ピクセルのPNG画像を用意
     - `iconutil`コマンドで変換：
       ```bash
       mkdir icon.iconset
       # 各サイズの画像をicon.iconsetに配置（icon_16x16.png, icon_32x32.pngなど）
       iconutil -c icns icon.iconset -o assets/icon.icns
       ```
     - または、オンラインツール（例: https://cloudconvert.com/png-to-icns）を使用

3. **ビルド**
   ```bash
   npm run dump streamlit_app
   npm run dist -- --mac
   ```

## ライセンス

receparserライブラリはMITライセンスです。
詳細は`streamlit_app/receparser/LICENSE.txt`を参照してください。

