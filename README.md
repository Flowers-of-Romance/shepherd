# shepherd

Claude Code の PostToolUse hook で動く崖っぷち検出。別の LLM が PLAN.md と照合して、エージェントが崖に向かっていたら通知する。

shepherd は、エージェントを自由に走らせて、崖に向かっているときだけ介入する。

## 仕組み

```
Claude Code がツールを実行
  ↓ PostToolUse hook
shepherd.py がチャンクに蓄積
  ↓ 閾値到達（デフォルト: 8回）
別の LLM (Gemini/Claude/Codex) にワンショットで判定させる
  ↓
far（草原）→ ログのみ
near（崖方向）→ トースト通知 + message.md
cliff（崖っぷち）→ トースト + LINE + message.md
```

## セットアップ

### 1. hook 登録

`.claude/settings.local.json` の PostToolUse に追加:

```json
{
  "type": "command",
  "command": "python C:/shepherd/shepherd.py",
  "timeout": 45000
}
```

### 2. PLAN.md を書く

```markdown
# Plan

## Goal
何をやるか

## Approach
どうやるか

## Boundaries
やってはいけないこと

<!-- shepherd: threshold=8 -->
<!-- shepherd: backend=gemini -->
```

shepherd は Boundaries を根拠に崖を判定する。具体的に書くほど精度が上がる。

### 3. LINE 通知（任意）

環境変数 `LINE_CHANNEL_TOKEN` をセットすると cliff 判定時に LINE broadcast で通知が飛ぶ。LINE Messaging API のチャネルアクセストークン（長期）が必要。

## バックエンド

PLAN.md の `<!-- shepherd: backend=xxx -->` で切り替え:

- `gemini` — Gemini CLI
- `claude` — Claude Code CLI
- `codex` — Codex CLI
- その他 — `{backend} -p ""` として実行

作業してるエージェントと検証するエージェントが別のモデルだと、迎合性が減る。

## 対話

shepherd は `message.md` にメッセージを書く。エージェントは `response.md` に返事を書く。次のチェック時に shepherd が返事を読む。ファイルを介した非同期の手紙。コンテキスト汚染ゼロ。

## ライセンス

CC0 1.0 Universal
