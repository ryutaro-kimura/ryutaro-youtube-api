from azure.functions import Blueprint, HttpRequest, HttpResponse

bp = Blueprint()

@bp.route(route="http_upload_video")
def http_upload_video(req: HttpRequest) -> HttpResponse:
    # 一旦文字列を返すだけの関数
    return HttpResponse("動画アップロードAPIのエンドポイントです。", status_code=200)
