import json
import logging
import os
import tempfile
from typing import Optional
from azure.functions import Blueprint, HttpRequest, HttpResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

bp = Blueprint()

# YouTube API スコープ
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service() -> Optional[object]:
    """YouTube Data API v3 サービスオブジェクトを取得"""
    try:
        # 環境変数から認証情報を取得
        client_id = os.environ.get('YOUTUBE_CLIENT_ID')
        client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
        refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
        
        if not all([client_id, client_secret, refresh_token]):
            logging.error("YouTube API認証情報が設定されていません")
            return None
        
        # 認証情報を作成
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        
        # トークンを更新
        if creds.expired:
            creds.refresh(Request())
        
        # YouTube Data API v3 サービスを構築
        youtube = build('youtube', 'v3', credentials=creds)
        return youtube
        
    except Exception as e:
        logging.error(f"YouTube API サービス初期化エラー: {str(e)}")
        return None

def upload_video_to_youtube(youtube, video_file_path: str, title: str, description: str = "", tags: list = None, privacy_status: str = "private") -> dict:
    """YouTubeに動画をアップロード"""
    try:
        # アップロード用のメタデータを設定
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': '22'  # People & Blogs カテゴリ
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }
        
        # ファイルアップロードを設定
        media = MediaFileUpload(
            video_file_path, 
            chunksize=-1, 
            resumable=True,
            mimetype='video/*'
        )
        
        # 動画をアップロード
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = insert_request.execute()
        
        return {
            'success': True,
            'video_id': response['id'],
            'title': response['snippet']['title'],
            'url': f"https://www.youtube.com/watch?v={response['id']}"
        }
        
    except HttpError as e:
        logging.error(f"YouTube API エラー: {e}")
        return {
            'success': False,
            'error': f"YouTube API エラー: {e}"
        }
    except Exception as e:
        logging.error(f"動画アップロードエラー: {e}")
        return {
            'success': False,
            'error': f"動画アップロードエラー: {e}"
        }

@bp.route(route="http_upload_video", methods=["POST"])
def http_upload_video(req: HttpRequest) -> HttpResponse:
    """YouTubeに動画をアップロードするHTTPエンドポイント"""
    
    try:
        # リクエストタイプをチェック
        if req.method != 'POST':
            return HttpResponse(
                json.dumps({'error': 'POSTメソッドのみサポートしています'}),
                status_code=405,
                mimetype='application/json; charset=utf-8'
            )
        
        # Content-Typeをチェック
        content_type = req.headers.get('content-type', '').lower()
        
        if 'multipart/form-data' in content_type:
            # マルチパートフォームデータからファイルとメタデータを取得
            files = req.files
            if not files or 'video' not in files:
                return HttpResponse(
                    json.dumps({'error': '動画ファイルが見つかりません。フィールド名は "video" を使用してください'}),
                    status_code=400,
                    mimetype='application/json; charset=utf-8'
                )
            
            video_file = files['video']
            
            # フォームデータからメタデータを取得
            title = req.form.get('title', 'Untitled Video')
            description = req.form.get('description', '')
            tags = req.form.get('tags', '').split(',') if req.form.get('tags') else []
            privacy_status = req.form.get('privacy_status', 'private')
            
        else:
            return HttpResponse(
                json.dumps({'error': 'multipart/form-dataのContent-Typeが必要です'}),
                status_code=400,
                mimetype='application/json; charset=utf-8'
            )
        
        # YouTube APIサービスを取得
        youtube = get_youtube_service()
        if not youtube:
            return HttpResponse(
                json.dumps({'error': 'YouTube API サービスの初期化に失敗しました'}),
                status_code=500,
                mimetype='application/json; charset=utf-8'
            )
        
        # 一時ファイルに動画を保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(video_file.read())
            temp_file_path = temp_file.name
        
        try:
            # YouTubeに動画をアップロード
            result = upload_video_to_youtube(
                youtube=youtube,
                video_file_path=temp_file_path,
                title=title,
                description=description,
                tags=tags,
                privacy_status=privacy_status
            )
            
            if result['success']:
                logging.info(f"動画アップロード成功: {result['video_id']}")
                return HttpResponse(
                    json.dumps({
                        'message': '動画のアップロードが完了しました',
                        'video_id': result['video_id'],
                        'title': result['title'],
                        'url': result['url']
                    }),
                    status_code=200,
                    mimetype='application/json; charset=utf-8'
                )
            else:
                logging.error(f"動画アップロード失敗: {result['error']}")
                return HttpResponse(
                    json.dumps({'error': result['error']}),
                    status_code=500,
                    mimetype='application/json; charset=utf-8'
                )
                
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
    except Exception as e:
        logging.error(f"予期しないエラー: {str(e)}")
        return HttpResponse(
            json.dumps({'error': f'予期しないエラー: {str(e)}'}),
            status_code=500,
            mimetype='application/json; charset=utf-8'
        )
