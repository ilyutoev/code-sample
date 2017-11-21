from django.views import generic
from news.models import News, Category


class IndexView(generic.ListView):
    model = News
    template_name = 'news/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['news_menu'] = True
        return context


class DetailView(generic.DetailView):
    model = News
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['news_menu'] = True
        return context


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'news/list.html'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return News.objects.filter(category=category)
        except Category.DoesNotExist:
            return News.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['news_menu'] = True
        try:
            context['category_name'] = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            pass
       
        return context
