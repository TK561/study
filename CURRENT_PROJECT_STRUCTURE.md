# 現在のプロジェクト構造

## メインファイル（使用中）

### 研究本体
- `api/index.py` - Vercel関数（研究成果表示）
- `vercel_api_setup.py` - Vercelデプロイ設定
- `index.html` - 静的HTML版
- `study/` - 研究データ

### Gemini統合システム
- `deep_consultation_system.py` - 深層相談システム（メイン）
- `claude_gemini_auto.py` - 自動相談機能
- `research_analysis_system.py` - 研究分析システム
- `interactive_analysis.py` - 対話的分析

### セッション復元システム
- `smart_recovery.py` - スマート復元（メイン）
- `session_recovery_system.py` - 復元システム本体
- `claude_auto_restore.py` - 自動復元機能
- `recover_claude_session.py` - 復元コマンド

## Claude Code用ファイル
- `TODAY_WORK_HANDOVER.md` - 作業引き継ぎ
- `QUICK_START_GUIDE.md` - 起動時ガイド
- `auto_save_today.py` - 作業内容自動保存

## セキュリティ
- `.env` - APIキー（非公開）
- `.claude_sessions/` - セッションデータ（ローカルのみ）

---
**最終更新**: 2025年06月22日 00:30
**整理状況**: 不要ファイル削除済み、構造最適化完了
