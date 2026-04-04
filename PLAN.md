# Plan

## Goal
memoriesテーブルを cortex（左脳）/ limbic（右脳）/ memories（脳梁）の3テーブルに物理分割する。

## Context
131箇所のSQL操作がmemoriesテーブルを参照している。全部を一度に書き換えるのはリスクが高い。
VIEWを使って後方互換を保ちつつ段階的に移行する。

## Approach

### テーブル構成

```
cortex (左脳)              limbic (右脳)              memories (脳梁/統合)
├ id PK (=memories.id)     ├ id PK (=memories.id)     ├ id PK AUTOINCREMENT
├ content TEXT NOT NULL     ├ emotions TEXT '[]'        ├ uuid TEXT UNIQUE
├ category TEXT 'fact'      ├ arousal REAL 0.2          ├ importance INTEGER 3
├ keywords TEXT '[]'        ├ flashbulb TEXT NULL       ├ created_at TEXT
├ embedding BLOB            ├ temporal_context TEXT     ├ updated_at TEXT
├ confidence REAL 0.7       ├ spatial_context TEXT      ├ last_accessed TEXT
├ provenance TEXT 'unknown' └                           ├ access_count INTEGER 0
├ revision_count INT 0                                  ├ forgotten INTEGER 0
├ merged_from TEXT NULL                                 ├ source_conversation TEXT
└                                                       ├ context_expires_at TEXT
                                                        ├ last_mutated TEXT
                                                        └
```

### VIEWによる後方互換

```sql
CREATE VIEW memories_v AS
SELECT m.id, c.content, c.category, m.importance,
       l.emotions, l.arousal, c.keywords,
       m.created_at, m.last_accessed, m.access_count, m.forgotten,
       m.source_conversation, c.embedding, c.merged_from,
       l.flashbulb, m.context_expires_at, l.temporal_context,
       l.spatial_context, m.uuid, m.updated_at, m.last_mutated,
       c.provenance, c.confidence, c.revision_count
FROM memories m
JOIN cortex c ON c.id = m.id
JOIN limbic l ON l.id = m.id;
```

### 移行戦略（3段階）

**Phase 1: テーブル作��� + データ移行**
1. cortex, limbic テーブルを CREATE
2. 既存memoriesからデータをコピー
3. memories_v VIEW を作成
4. init_db() にマイグレーションを��加

**Phase 2: INSERT/UPDATE パスの更新**
1. add_memory() — 3テーブルに分けてINSERT
2. consolidate_memories() — 3テーブルに分けてINSERT
3. build_schemas() — 同上
4. correct_memory() — cortexのみUPDATE
5. interfere() �� limbicとmemoriesをUPDATE
6. sync_import() — 3テーブルに分けてINSERT/UPDATE
7. その他のUPDATE文を対象テーブルに振り分け

**Phase 3: SELECT パスの更新**
1. `SELECT * FROM memories` → `SELECT * FROM memories_v`
2. 左脳だけで十分な箇所 → `SELECT ... FROM cortex JOIN memories ...`
3. 右脳だけで十分な箇所 → `SELECT ... FROM limbic JOIN memories ...`
4. _left_score / _right_score が各テーブルから直接読め���構造に

### 移行の安全策
- memories テーブルの旧カラムは削除し��い（フォールバック）
- memories_v VIEW が旧スキーマと同一カラム名を返す
- 全操���後に `python memory.py recall` で動作確認

## Boundaries
- memory.py のみ変更
- 既存データを壊さない
- VIEW で後方互換を保つ — 131箇所を一度に全部書き換えない
- Phase 1 で止めても動く状態を維持

## Current Phase
Phase 1+2 完了。Phase 3（SELECT→VIEW切り替え）は段階的に実施。

<!-- shepherd: threshold=8 -->
<!-- shepherd: backend=gemini -->
