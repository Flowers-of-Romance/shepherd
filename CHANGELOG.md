# Changelog

## [v1.2] - 2026-04-11

### Added
- **ダッシュボード**: `python dashboard_server.py` で localhost:8385 にTrello風カンバンボードを起動
- **3ビュー**: Board（far/near/cliff 3カラム）、Timeline（全履歴の時系列表示）、PLAN.md（全文表示）
- **GNU風の羊**: ブロック文字 `▄███▄` で描いた羊がfar(°_°)/near(O_O)/cliff(X_X)で表情変化。cliffで震える
- **自動更新**: 5秒ごとにfetchしてリアルタイム反映
- **ヘッダー**: 最新判定インジケーター、far/near/cliff比率バー、ACTIVE/OFFバッジ

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
