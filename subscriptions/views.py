# Create your views here.
import logging
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription
from .forms import InquiryForm, SubscriptionForm
from .models import Service, Category

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
        qs = Subscription.objects.filter(user=self.request.user)\
            .select_related('service', 'service__category')

        group = self.request.GET.get("group")

        if group:
            qs = qs.filter(service__category__group=group)

        return qs.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Category.objects.values_list('group', flat=True).distinct()

        return context

# サブスクテーブルから必要なデータを取得してテンプレートを描画
class SubscriptionDetailView(LoginRequiredMixin,generic.DetailView):
    model = Subscription
    template_name = 'subscriptions/subscription_detail.html'
    # 例えば、pkをidに変更したい場合には以下のように記述する
    # pk_url_kwarg = 'id'
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)\
            .select_related('service', 'service__category')\
            .order_by('start_date')


class SubscriptionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Subscription
    template_name = 'subscriptions/subscription_create.html'
    form_class = SubscriptionForm # form_classをオーバーライドしてフォームを利用することを宣言
    success_url = reverse_lazy('subscriptions:subscription_list') # 正常に処理が完了した際の遷移先

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'サブスクを登録しました')
        return super().form_valid(form)
        
    def form_invalid(self, form): # フォームバリデーションが失敗した時に実行されるメソッド
        messages.error(self.request, "サブスクの登録に失敗しました")
        return self.render_to_response(self.get_context_data(form=form))

class SubscriptionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Subscription
    template_name = 'subscriptions/subscription_update.html'
    form_class = SubscriptionForm

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)\
            .select_related('service', 'service__category')\
            .order_by('start_date')

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
        return Subscription.objects.filter(user=self.request.user)\
            .select_related('service', 'service__category')\
            .order_by('start_date')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "サブスクを削除しました")
        return super().delete(request, *args, **kwargs)


class SoonSubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_soon.html'
    paginate_by = 5

    def get_queryset(self):
        subs = Subscription.objects.filter(user=self.request.user)\
            .select_related('service', 'service__category')

        soon_subs = [sub for sub in subs if sub.is_soon()]
        return sorted(soon_subs, key=lambda x: x.next_renewal_date())
    