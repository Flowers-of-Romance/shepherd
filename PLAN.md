# PLAN.md

shepherd はこのファイルと作業ログを照合して崖判定する。

## 書き方

```markdown
## Goal
何を達成するか

## Approach
どういうやり方で進めるか

## Boundaries
やってはいけないこと（shepherd はここを根拠に崖を判定する）

## Current Phase
今どの段階にいるか
```

## 設定

HTML コメントで shepherd の動作を制御できる:

```
<!-- shepherd: threshold=8 -->    チェック間隔（ツール呼び出し回数）
<!-- shepherd: backend=gemini -->  判定に使う LLM (gemini/claude/codex)
```

## 例

```markdown
# Plan

## Goal
認証ミドルウェアを JWT から OAuth2 に移行する

## Approach
- auth/ 配下のみ変更
- 既存テストを通し続ける
- 段階的に移行

## Boundaries
- DB スキーマを変えない
- ユーザー向け API のレスポンス形式を変えない
- rm コマンドを使わない

## Current Phase
auth/middleware.py のリファクタリング中

<!-- shepherd: threshold=10 -->
<!-- shepherd: backend=gemini -->
```
