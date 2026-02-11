# Create your views here.

from django.views import generic

# TemplateView)　→ トップページは静的ページであるためテンプレートの表示に特化したtemplateViewびゅーを使用
# template_name → どのクラスベースビューでも共通で共通で持っているクラス変数、設定するのが必須
class indexView(generic.TemplateView):
    template_name = "index.html"