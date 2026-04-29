# Create your views here.
import logging
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription
from .forms import InquiryForm, SubscriptionForm
from .models import Service

logger = logging.getLogger(__name__)

# TemplateView)　→ トップページは静的ページであるためテンプレートの表示に特化したtemplateViewビューを使用
# template_name → どのクラスベースビューでも共通で共通で持っているクラス変数、設定するのが必須
class IndexView(generic.TemplateView):
    template_name = "subscriptions/index.html"

class InquiryView(generic.FormView):
    template_name = "subscriptions/inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('subscriptions:inquiry')

    def form_valid(self,form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
    
# サブスク一覧を表示させるためのクラス
class SubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        context['subscription_list'] = sorted(
            context['subscription_list'],
            key=lambda x: (
                x.next_renewal_date() < today,
                x.next_renewal_date()
            )
        )

        return context

# サブスクテーブルから必要なデータを取得してテンプレートを描画
class SubscriptionDetailView(LoginRequiredMixin,generic.DetailView):
    model = Subscription
    template_name = 'subscriptions/subscription_detail.html'
    # 例えば、pkをidに変更したい場合には以下のように記述する
    # pk_url_kwarg = 'id'
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class SubscriptionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Subscription
    template_name = 'subscriptions/subscription_create.html'
    form_class = SubscriptionForm # form_classをオーバーライドしてフォームを利用することを宣言
    success_url = reverse_lazy('subscriptions:subscription_list') # 正常に処理が完了した際の遷移先

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

    def form_valid(self, form): # フォームの入力値に問題がなければ実行されるメソッド
        sub = form.save(commit=False) # ユーザ入力値だけでは不足がある場合DBには保存しないDiaryを取得
        sub.user = self.request.user # ログインしているユーザのモデルオブジェクトをセット
        sub.save() # ここでDBに保存
        messages.success(self.request, 'サブスクを登録しました')

        self.object = sub
        return super().form_valid(form)
    
    def form_invalid(self, form): # フォームバリデーションが失敗した時に実行されるメソッド
        messages.error(self.request, "サブスクの登録に失敗しました")
        return self.render_to_response(self.get_context_data(form=form))

class SubscriptionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Subscription
    template_name = 'subscriptions/subscription_update.html'
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def  get_success_url(self):
        return reverse_lazy('subscriptions:subscription_detail',kwargs={'pk': self.kwargs['pk']})
        
    def form_valid(self, form):
        messages.success(self.request,'サブスク登録を更新しました')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'サブスク登録の更新に失敗しました')
        return super().form_invalid(form)
    

    
class SubscriptionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Subscription
    template_name = 'subscriptions/subscription_delete.html'
    success_url = reverse_lazy('subscriptions:subscription_list')

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "サブスクを削除しました")
        return super().delete(request, *args, **kwargs)


class SoonSubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_soon.html'
    paginate_by = 5

    def get_queryset(self):
        subs = Subscription.objects.filter(user=self.request.user)

        soon_subs = [sub for sub in subs if sub.is_soon()]
        return sorted(soon_subs, key=lambda x: x.next_renewal_date())
    