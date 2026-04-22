from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# あとでホストを変更
ALLOWED_HOSTS = ['*']

# ロギング設定
LOGGING = {
    'version': 1, # 1 固定
    'disable_existing_loggers':False,
    # ロガーの設定
    'loggers':{
        # djangoが設定するロガー
        'django':{
            'handlers':['console'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary':{
            'handlers':['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers':{
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter':'dev'
        },
    },
    # フォーマッたの設定
    'formatters':{
        'dev': {
            'format':'\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(line:%(lineno)d)',
                '%(message)s'
            ]) 
        },
    },    
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 2026-03-04追加
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 2026-3-27追加　セキュリティ設定
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 2026-3-27追加　静的ファイル設定
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


