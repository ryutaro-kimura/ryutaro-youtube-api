# Conventional Commits ルール

このプロジェクトでは、コミットメッセージに [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) のルールを採用します。

## フォーマット
コミットメッセージは以下のフォーマットに従ってください。

<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

### type の例
- feat: 新機能の追加
- fix: バグ修正
- docs: ドキュメントのみの変更
- style: フォーマットの修正（コードの動作に影響しない変更）
- refactor: リファクタリング（機能追加やバグ修正を含まない変更）
- perf: パフォーマンス向上のための変更
- test: テストコードの追加や修正
- chore: ビルドプロセスや補助ツール、ライブラリの変更

### 絵文字の例
コミットメッセージの先頭に、以下のような絵文字を type と組み合わせて使うこともできます。

- ✨ feat: 新機能の追加
- 🐛 fix: バグ修正
- 📝 docs: ドキュメントのみの変更
- 💄 style: フォーマットの修正（コードの動作に影響しない変更）
- ♻️ refactor: リファクタリング（機能追加やバグ修正を含まない変更）
- ⚡️ perf: パフォーマンス向上のための変更
- ✅ test: テストコードの追加や修正
- 🔧 chore: ビルドプロセスや補助ツール、ライブラリの変更

例:  
`✨ feat: ユーザー認証機能を追加`