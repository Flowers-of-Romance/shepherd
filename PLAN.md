# Shepherd Dashboard — ブラウザで見れるTrello的ボード

## Goal

shepherd_log.jsonlとPLAN.mdのデータをブラウザ上でTrello風カンバンボードとして可視化する。
リアルタイムでshepherdの状態を俯瞰できるダッシュボード。

## Approach

**単一HTMLファイル**（`C:/shepherd/dashboard.html`）+ 小さなサーバー（`dashboard_server.py`）。

### カラム構成（Trello風3列）
1. **草原 (far)** — 安全。直近のfar判定をカードで表示
2. **崖方向 (near)** — 警告。near判定をカードで表示
3. **崖っぷち (cliff)** — 危険。cliff判定をカードで表示

### カード内容
- タイムスタンプ（相対時刻: "3分前"等）
- reason（判定理由）
- chunk_lines数
- 距離に応じた色分け（緑/黄/赤）

### ヘッダー
- 現在のPLAN.md Goal を表示
- 現在のPhase
- 最新の判定距離をインジケーター表示（緑/黄/赤の丸）
- 統計: far/near/cliff の比率バー

### データ配信（`dashboard_server.py`）
- `localhost:8384` で起動
- `/` → dashboard.html
- `/api/log` → shepherd_log.jsonl を JSON配列で返す（直近100件）
- `/api/plan` → PLAN.mdをパースしてGoal/Phase等を返す
- `/api/status` → chunk_count, cliff_warning, shepherd-active等のリアルタイム状態

### 自動更新
- 5秒ごとにfetchしてカードを差分更新

### 技術
- HTML + CSS + vanilla JS（依存ゼロ）
- CSS Grid で3カラムレイアウト
- 読み取り専用（操作なし）

## Boundaries

- 外部依存なし（npm, CDN, framework一切なし）
- shepherd.py は変更しない
- ファイルは2つだけ: `dashboard.html` + `dashboard_server.py`
- データの書き込みはしない（読み取り専用）

## Current Phase

完了

<!-- shepherd: threshold=3 -->
<!-- shepherd: backend=claude -->
