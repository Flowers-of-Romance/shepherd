# Plan

## Goal
外部モニターの輝度を調整するCLIアプリを作る。
起動時に現在の輝度を取得 → ユーザーが好きな輝度に変更 → 終了時に元の輝度に復元。

## Approach
- Python + monitorcontrol ライブラリ（DDC/CI）
- C:\brightness に独立フォルダとして作る
- CLIのみ、GUIなし
- 単一ファイル（brightness.py）で完結させる

## Boundaries
- C:\memory のコードを変更しない
- C:\shepherd のコード（shepherd.py）を変更しない
- GUIフレームワークを入れない
- 外部モニターのDDC/CI以外の方法（WMI等）は使わない
- 管理者権限なしで動くようにする
- rm コマンドを使わない（ファイル削除禁止）

## Current Phase
初期実装。monitorcontrolのインストールと基本機能の実装。

<!-- shepherd: threshold=5 -->
<!-- shepherd: backend=gemini -->
