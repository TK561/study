#!/usr/bin/env python3
"""
研究プロジェクト用Streamlitアプリ
Vercelデプロイ対応版
"""

import streamlit as st
import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """メインアプリケーション"""
    st.set_page_config(
        page_title="研究プロジェクト管理システム",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("研究プロジェクト管理システム")
    st.markdown("---")
    
    # サイドバー
    st.sidebar.title("メニュー")
    page = st.sidebar.selectbox(
        "ページを選択",
        ["ホーム", "セッション管理", "プロジェクト概要", "Git状況"]
    )
    
    if page == "ホーム":
        show_home()
    elif page == "セッション管理":
        show_session_management()
    elif page == "プロジェクト概要":
        show_project_overview()
    elif page == "Git状況":
        show_git_status()

def show_home():
    """ホームページ"""
    st.header("研究プロジェクト管理システム")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("プロジェクト情報")
        st.write("**名前**: 意味カテゴリに基づく画像分類システム")
        st.write("**目的**: WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価")
        st.write("**開発手法**: Claude Code を活用したAI支援研究開発")
    
    with col2:
        st.subheader("システム状況")
        st.success("システム稼働中")
        st.info("1時間毎作業整理システム: 有効")
        st.info("セキュリティ対策: 完了")

def show_session_management():
    """セッション管理ページ"""
    st.header("セッション管理")
    
    # セッションログの表示
    session_logs_dir = project_root / "session_logs"
    
    if session_logs_dir.exists():
        log_files = list(session_logs_dir.glob("*.json"))
        
        if log_files:
            st.subheader("セッションログ")
            selected_log = st.selectbox("ログファイルを選択", log_files)
            
            if selected_log:
                try:
                    import json
                    with open(selected_log, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                    
                    st.json(session_data)
                except Exception as e:
                    st.error(f"ログファイル読み込みエラー: {e}")
        else:
            st.info("セッションログがありません")
    else:
        st.info("session_logsディレクトリが存在しません")
    
    # 統合レポートの表示
    consolidated_report = session_logs_dir / "consolidated_work_summary.md" if session_logs_dir.exists() else None
    
    if consolidated_report and consolidated_report.exists():
        st.subheader("統合作業レポート")
        with open(consolidated_report, 'r', encoding='utf-8') as f:
            report_content = f.read()
        st.markdown(report_content)
    else:
        st.info("統合レポートがありません")

def show_project_overview():
    """プロジェクト概要ページ"""
    st.header("プロジェクト概要")
    
    # ファイル構造の表示
    st.subheader("プロジェクト構造")
    
    def show_file_tree(directory, prefix="", max_depth=3, current_depth=0):
        """ファイルツリーを表示"""
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(directory.iterdir())
            for item in items:
                if item.name.startswith('.') and item.name not in ['.env.example', '.gitignore']:
                    continue
                
                if item.is_dir():
                    st.text(f"{prefix}📁 {item.name}/")
                    if current_depth < max_depth - 1:
                        show_file_tree(item, prefix + "  ", max_depth, current_depth + 1)
                else:
                    st.text(f"{prefix}📄 {item.name}")
        except PermissionError:
            st.text(f"{prefix}❌ アクセス権限がありません")
    
    show_file_tree(project_root)
    
    # 主要ファイルの説明
    st.subheader("主要ファイル")
    
    file_descriptions = {
        "semantic_classification_system.py": "メインの統合分類システム",
        "research_git_automation.py": "研究用Git自動化システム",
        "secure_config.py": "セキュアな設定管理システム",
        "hourly_summary_system.py": "1時間毎作業整理システム",
        "CLAUDE.md": "Claude Code 設定ファイル",
        "SECURITY.md": "セキュリティガイドライン"
    }
    
    for filename, description in file_descriptions.items():
        file_path = project_root / filename
        if file_path.exists():
            st.write(f"**{filename}**: {description}")

def show_git_status():
    """Git状況ページ"""
    st.header("Git状況")
    
    try:
        import subprocess
        
        # Git status
        st.subheader("作業ディレクトリ状況")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.stdout.strip():
            st.text("変更されたファイル:")
            st.code(result.stdout)
        else:
            st.success("作業ディレクトリはクリーンです")
        
        # Recent commits
        st.subheader("最近のコミット")
        result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.stdout:
            st.code(result.stdout)
        
        # Branch info
        st.subheader("ブランチ情報")
        result = subprocess.run(['git', 'branch', '-v'], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.stdout:
            st.code(result.stdout)
            
    except Exception as e:
        st.error(f"Git情報取得エラー: {e}")

if __name__ == "__main__":
    main()