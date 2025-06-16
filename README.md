# YouTube Video Upload API

Azure Functions アプリケーションで YouTube に動画をアップロードするための API です。

## 機能

- YouTube Data API v3 を使用した動画アップロード
- マルチパートフォームデータでの動画ファイルアップロード
- 動画のメタデータ（タイトル、説明、タグ、プライバシー設定）の指定
- エラーハンドリングと適切なレスポンス

## 必要な環境変数

YouTube API を使用するために、以下の環境変数を設定してください：

```
YOUTUBE_CLIENT_ID=your_youtube_api_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_api_client_secret
YOUTUBE_REFRESH_TOKEN=your_youtube_api_refresh_token
```

### YouTube API 認証情報の取得方法

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. YouTube Data API v3 を有効化
3. OAuth 2.0 認証情報を作成
4. リフレッシュトークンを取得

## API エンドポイント

### POST /api/http_upload_video

YouTube に動画をアップロードします。

#### リクエスト形式

- Content-Type: `multipart/form-data`

#### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| video | file | ✓ | アップロードする動画ファイル |
| title | string | | 動画のタイトル（デフォルト: "Untitled Video"） |
| description | string | | 動画の説明 |
| tags | string | | カンマ区切りのタグ |
| privacy_status | string | | プライバシー設定（private, public, unlisted）（デフォルト: "private"） |

#### レスポンス例

成功時：
```json
{
  "message": "動画のアップロードが完了しました",
  "video_id": "dQw4w9WgXcQ",
  "title": "Sample Video",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

エラー時：
```json
{
  "error": "エラーメッセージ"
}
```

## 使用例

### curl を使用した例

```bash
curl -X POST \
  -F "video=@sample_video.mp4" \
  -F "title=My Sample Video" \
  -F "description=This is a sample video upload" \
  -F "tags=sample,test,demo" \
  -F "privacy_status=private" \
  https://your-function-app.azurewebsites.net/api/http_upload_video
```

## エラーコード

| ステータスコード | 説明 |
|-----------------|------|
| 200 | 成功 |
| 400 | リクエストエラー（ファイルなし、Content-Type不正など） |
| 405 | メソッドエラー（POSTのみサポート） |
| 500 | サーバーエラー（YouTube API エラーなど） |

## 開発とテスト

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 基本的な動作確認

```bash
python /tmp/test_upload_function.py
```

## 注意事項

- YouTube API には利用制限があります
- アップロードされる動画は指定されたプライバシー設定で公開されます
- 大きなファイルのアップロードには時間がかかる場合があります
- 認証情報は安全に管理してください