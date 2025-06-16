import azure.functions as func
import logging
from http_upload_video import bp as http_upload_video_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_functions(http_upload_video_bp)