import streamlit as st
import pandas as pd
import tempfile
import os
import sys
import json
from pathlib import Path

# Add receparser directory to Python path
receparser_path = Path(__file__).parent / "receparser"
if str(receparser_path) not in sys.path:
    sys.path.insert(0, str(receparser_path))

from receparser import MonthlyRece

# Helper function to get patient info from RE record
def get_rece_info(rece):
    """Get patient info from a Rece object"""
    try:
        re_records = rece['RE']
        if isinstance(re_records, list) and len(re_records) > 0:
            re_record = re_records[0]
            return {
                '氏名': re_record.get('氏名', ''),
                'カタカナ氏名': re_record.get('カタカナ氏名', ''),
                '生年月日': re_record.get('生年月日', ''),
                '男女区分': re_record.get('男女区分', ''),
                '診療年月': re_record.get('診療年月', ''),
                'レセプト番号': re_record.get('レセプト番号', ''),
            }
    except (KeyError, TypeError):
        # Fallback: search in rece_list
        for record in rece.rece_list:
            record_type = record.get('レコード識別情報') or record.get('レコード識別番号')
            if record_type == 'RE':
                return {
                    '氏名': record.get('氏名', ''),
                    'カタカナ氏名': record.get('カタカナ氏名', ''),
                    '生年月日': record.get('生年月日', ''),
                    '男女区分': record.get('男女区分', ''),
                    '診療年月': record.get('診療年月', ''),
                    'レセプト番号': record.get('レセプト番号', ''),
                }
    return {
        '氏名': '',
        'カタカナ氏名': '',
        '生年月日': '',
        '男女区分': '',
        '診療年月': '',
        'レセプト番号': '',
    }


st.set_page_config(
    page_title="Receparser Online",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Receparser Online")
st.markdown("電子レセプトファイルをアップロードして可視化します")

# Sidebar for file upload and settings
with st.sidebar:
    st.header("ファイル設定")
    
    uploaded_file = st.file_uploader(
        "レセプトファイルをアップロード",
        type=['csv', 'txt', 'UKE'],
        help="Shift-JISエンコーディングのCSVファイルをアップロードしてください"
    )
    
    receipt_type = st.radio(
        "レセプトタイプ",
        ["医科", "DPC"],
        help="DPCレセプトまたは医科レセプトを選択してください"
    )

# Main content area
if uploaded_file is not None:
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Parse the receipt file
            codes = "dpc" if receipt_type == "DPC" else "ika"
            monthly_rece = MonthlyRece(tmp_path, codes=codes)
            
            # Get all chart numbers
            chart_numbers = list(monthly_rece.keys())
            
            if not chart_numbers:
                st.warning("レセプトデータが見つかりませんでした。")
            else:
                st.success(f"✅ {len(chart_numbers)}件のレセプトデータを読み込みました")
                
                
                # Build patient list - each receipt as a separate row
                patient_list = []
                for chart_num in chart_numbers:
                    rece_list = monthly_rece[chart_num]
                    for rece_idx, rece in enumerate(rece_list):
                        info = get_rece_info(rece)
                        patient_list.append({
                            'カルテ番号': chart_num if chart_num else '未設定',
                            'レセプト番号': info['レセプト番号'],
                            'レセプトインデックス': rece_idx,
                            '氏名': info['氏名'],
                            'カタカナ氏名': info['カタカナ氏名'],
                            '生年月日': info['生年月日'],
                            '男女区分': info['男女区分'],
                            '診療年月': info['診療年月'],
                        })
                
                patient_df = pd.DataFrame(patient_list)
                
                # Patient search and selection
                st.header("👥 患者一覧")
                
                # Search box
                search_query = st.text_input(
                    "🔍 レセプトを検索（氏名、カタカナ氏名、カルテ番号、レセプト番号で検索）",
                    placeholder="検索キーワードを入力..."
                )
                
                # Filter receipts based on search
                if search_query:
                    mask = (
                        patient_df['氏名'].str.contains(search_query, case=False, na=False) |
                        patient_df['カタカナ氏名'].str.contains(search_query, case=False, na=False) |
                        patient_df['カルテ番号'].astype(str).str.contains(search_query, case=False, na=False) |
                        patient_df['レセプト番号'].astype(str).str.contains(search_query, case=False, na=False)
                    )
                    filtered_df = patient_df[mask]
                else:
                    filtered_df = patient_df
                
                # Display patient list
                if len(filtered_df) > 0:
                    st.info(f"📊 {len(filtered_df)}件のレセプトが見つかりました（全{len(patient_df)}件中）")
                    
                    # Display patient table
                    display_df = filtered_df[['カルテ番号', 'レセプト番号', '氏名', 'カタカナ氏名', '生年月日', '男女区分', '診療年月']].copy()
                    st.dataframe(
                        display_df,
                        width='stretch',
                        height=300,
                        hide_index=True
                    )
                    
                    # Patient selection
                    if len(filtered_df) == 1:
                        selected_row = filtered_df.iloc[0]
                        selected_chart = selected_row['カルテ番号']
                        selected_rece_idx = selected_row['レセプトインデックス']
                    else:
                        # Create selection options
                        patient_options = []
                        for idx in range(len(filtered_df)):
                            row = filtered_df.iloc[idx]
                            name = row['氏名'] if row['氏名'] else '（氏名なし）'
                            chart = row['カルテ番号']
                            rece_num = row['レセプト番号'] if row['レセプト番号'] else f"レセプト{row['レセプトインデックス']+1}"
                            option_text = f"{chart} - {name} (レセプト番号: {rece_num})"
                            patient_options.append((idx, option_text, chart, row['レセプトインデックス']))
                        
                        selected_option = st.selectbox(
                            "レセプトを選択",
                            range(len(patient_options)),
                            format_func=lambda x: patient_options[x][1]
                        )
                        selected_chart = patient_options[selected_option][2]
                        selected_rece_idx = patient_options[selected_option][3]
                    
                else:
                    st.warning("検索条件に一致するレセプトが見つかりませんでした。")
                    selected_chart = None
                    selected_rece_idx = None
                
                if selected_chart is not None and selected_chart != '未設定' and selected_rece_idx is not None:
                    st.divider()
                    
                    # Get Rece objects for selected chart number
                    # Convert '未設定' back to empty string for lookup
                    chart_key = '' if selected_chart == '未設定' else selected_chart
                    rece_list = monthly_rece[chart_key]
                    
                    # Get the specific receipt
                    rece = rece_list[selected_rece_idx]
                    
                    # Get patient info for display
                    patient_info = get_rece_info(rece)
                    
                    # Display header with receipt number
                    rece_num = patient_info['レセプト番号'] if patient_info['レセプト番号'] else f"レセプト{selected_rece_idx+1}"
                    st.header(f"📋 患者データ: {selected_chart} (レセプト番号: {rece_num})")
                    
                    if rece:
                        # Export all records as JSON or Markdown (foldable, collapsed by default)
                        with st.expander("📤 全レコードをエクスポート (JSON/Markdown)", expanded=False):
                            export_format = st.radio(
                                "エクスポート形式",
                                ["JSON", "Markdown"],
                                horizontal=True,
                                help="全レコードをJSONまたはMarkdown形式でコピーできます"
                            )
                            
                            # Collect all records
                            all_records_data = {}
                            for record in rece.rece_list:
                                record_type = record.get('レコード識別情報') or record.get('レコード識別番号')
                                if record_type:
                                    if record_type not in all_records_data:
                                        all_records_data[record_type] = []
                                    all_records_data[record_type].append(record)
                            
                            if export_format == "JSON":
                                # Convert to JSON
                                json_output = json.dumps(all_records_data, ensure_ascii=False, indent=2)
                                st.code(json_output, language='json')
                            else:
                                # Convert to Markdown
                                markdown_lines = []
                                markdown_lines.append(f"# 患者データ: {selected_chart} (レセプト番号: {rece_num})\n")
                                
                                for record_type, records in sorted(all_records_data.items()):
                                    markdown_lines.append(f"## {record_type}レコード\n")
                                    for idx, record in enumerate(records, 1):
                                        markdown_lines.append(f"### {record_type}レコード {idx}\n")
                                        markdown_lines.append("| 項目 | 値 |\n")
                                        markdown_lines.append("|------|-----|\n")
                                        for key, value in record.items():
                                            if key:  # Skip None keys
                                                markdown_lines.append(f"| {key} | {value if value else ''} |\n")
                                        markdown_lines.append("\n")
                                
                                markdown_output = "".join(markdown_lines)
                                st.code(markdown_output, language='markdown')
                        # Display patient info
                        if patient_info['氏名']:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("氏名", patient_info['氏名'])
                            if patient_info['カタカナ氏名']:
                                with col2:
                                    st.metric("カタカナ氏名", patient_info['カタカナ氏名'])
                            if patient_info['生年月日']:
                                with col3:
                                    st.metric("生年月日", patient_info['生年月日'])
                        
                        # Collect all record types from the selected receipt
                        all_record_types = set()
                        all_records_by_type = {}
                        
                        # Get available record types from the selected receipt
                        for record in rece.rece_list:
                            record_type = record.get('レコード識別情報') or record.get('レコード識別番号')
                            if record_type:
                                all_record_types.add(record_type)
                                if record_type not in all_records_by_type:
                                    all_records_by_type[record_type] = []
                                all_records_by_type[record_type].append(record)
                        
                        record_types = sorted(list(all_record_types))
                        
                        if record_types:                            
                            # Display all record types vertically
                            for record_type in record_types:
                                records = all_records_by_type[record_type]
                                
                                if records:
                                    # Record type header
                                    st.markdown(f"### 📄 {record_type}レコード")
                                    
                                    # Convert to DataFrame
                                    df = pd.DataFrame(records)
                                    
                                    # Fix column names: convert None to empty string and ensure all are strings
                                    df.columns = [str(col) if col is not None else '' for col in df.columns]
                                    
                                    # Display DataFrame
                                    st.dataframe(df, width='stretch', height=400)
                                    
                                    # Download button
                                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                                    st.download_button(
                                        label=f"📥 {record_type}レコードをCSVとしてダウンロード",
                                        data=csv,
                                        file_name=f"{selected_chart}_{record_type}.csv",
                                        mime="text/csv",
                                        key=f"download_{record_type}"
                                    )
                                    
                                    # Add separator between record types
                                    st.divider()
                                else:
                                    st.markdown(f"### 📄 {record_type}レコード")
                                    st.info(f"レコードタイプ '{record_type}' のデータがありません。")
                                    st.divider()
                            
                        else:
                            st.warning("レコードタイプが見つかりませんでした。")
                    else:
                        st.warning("選択されたカルテ番号に対応するレセプトデータがありません。")
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.exception(e)
else:
    # Show instructions when no file is uploaded
    st.info("👈 左側のサイドバーからレセプトファイルをアップロードしてください")
    
    st.markdown("""
    ### 使い方
    
    1. **ファイルをアップロード**: 左側のサイドバーからレセプトファイル（CSV形式、Shift-JISエンコーディング）をアップロードします
    2. **レセプトタイプを選択**: DPCレセプトまたは医科レセプトを選択します
    3. **カルテ番号を選択**: 読み込まれたレセプトから表示したいカルテ番号を選択します
    4. **レコードタイプを選択**: 表示したいレコードタイプ（RE, HO, SBなど）を選択します
    5. **データを確認**: テーブル形式でデータを確認し、必要に応じてCSVとしてダウンロードできます
    
    ### 対応レコードタイプ
    
    - **RE**: レセプト共通レコード
    - **HO**: 公費レコード
    - **SB**: 傷病名レコード
    - **KO**: コメントレコード
    - その他、レセプトファイルに含まれるすべてのレコードタイプ
    """)


