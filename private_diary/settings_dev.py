from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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

# どうやって送るか
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 本番ではこっち

# 2026-03-04追加ß
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')