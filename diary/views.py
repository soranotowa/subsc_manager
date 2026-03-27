# Create your views here.
import logging
from django.urls import reverse_lazy

from django.views import generic
from .forms import InquiryForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary
from .forms import InquiryForm, DiaryCreateForm

logger = logging.getLogger(__name__)

# TemplateView)　→ トップページは静的ページであるためテンプレートの表示に特化したtemplateViewビューを使用
# template_name → どのクラスベースビューでも共通で共通で持っているクラス変数、設定するのが必須
class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self,form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
    
# 日記一覧を表示させるためのクラス
class DiaryListView(LoginRequiredMixin,generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries
        # 実務では以下のように書くのだそうだ　変数 diaries を作る必要がないため
        # return Diary.objects.filter(user=self.request.user).order_by('-created_at')

# Diaryテーブルから必要なデータを取得してテンプレートを描画
class DiaryDetailView(LoginRequiredMixin,generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'
    # 例えば、pkをidに変更したい場合には以下のように記述する
    # pk_url_kwarg = 'id'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm # form_classをオーバーライドしてフォームを利用することを宣言
    success_url = reverse_lazy('diary:diary_list') # 正常に処理が完了した際の遷移先

    def form_valid(self, form): # フォームの入力値に問題がなければ実行されるメソッド
        diary = form.save(commit=False) # ユーザ入力値だけでは不足がある場合DBには保存しないDiaryを取得
        diary.user = self.request.user # ログインしているユーザのモデルオブジェクトをセット
        diary.save() # ここでDBに保存
        messages.success(self.request, '日記を作成しました')

        self.object = diary
        return super().form_valid(form)
    
    
    def form_invalid(self, form): # フォームバリデーションが失敗した時に実行されるメソッド
        messages.error(self.request, "日記の作成に失敗しました")
        # return super().form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def  get_success_url(self):
        return reverse_lazy('diary:diary_detail',kwargs={'pk': self.kwargs['pk']})
        
    def form_valid(self, form):
        messages.success(self.request,'日記を更新しました')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'日記の更新に失敗しました')
        return super().form_invalid(form)
    
class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました")
        return super().delete(request, *args, **kwargs)


    