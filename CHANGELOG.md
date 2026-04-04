# Changelog

## [v1.1] - 2026-04-04

### Added
- **`/lsd` スキル**: shepherd崖検出を起動。hookの自動登録、tempバッファリセット、ステータスラインマーカー作成、設計→承認→実装のフローを強制
- **`/sober` スキル**: shepherd崖検出を停止。hookの除去、tempバッファクリーンアップ、ステータスラインマーカー削除
- **`/verify` コマンド**: PLAN.mdと現在の作業の整合性を自己検証。far（草原）/ near（崖方向）/ cliff（崖っぷち）の3段階判定。shepherdのmessage.mdとも連携

## [v1.0] - 2026-03-30

### Added
- **shepherd.py**: PostToolUse hookでチャンクを蓄積し、閾値到達時に別LLMでワンショット判定
- **崖検出**: far / near / cliff の3段階。Boundariesを根拠に判定
- **バックエンド切替**: Gemini / Claude / Codex をPLAN.mdのコメントで指定
- **通知**: トースト通知 + LINE broadcast（cliff時）
- **非同期対話**: message.md / response.md によるファイル経由の手紙
