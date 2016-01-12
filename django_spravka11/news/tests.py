from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from news.models import News, Category

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class NewsTest(TestCase):
    def test_create_category(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category, category)

        self.assertEquals(only_category.name, 'Экономика')
        self.assertEquals(only_category.description, 'Новости экономики')

    def test_create_news(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        #создаем новость и заполняем поля
        news = News()

        #устанавливаем атрибуты
        news.title = 'Моя первая новость'
        news.announcement = 'Анонс первой новости ++'
        news.text = 'Текст первой новости!!!'
        news.pub_date = timezone.now()
        news.category = category

        #сохраняем в бд
        news.save()

        #проверяем что новость доавбилась в базу
        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)
        only_news = all_news[0]
        self.assertEquals(only_news, news)

        #проверяем атрибуты
        self.assertEquals(only_news.title, 'Моя первая новость')
        self.assertEquals(only_news.announcement, 'Анонс первой новости ++')
        self.assertEquals(only_news.text, 'Текст первой новости!!!')
        self.assertEquals(only_news.pub_date.day, news.pub_date.day)
        self.assertEquals(only_news.pub_date.month, news.pub_date.month)
        self.assertEquals(only_news.pub_date.year, news.pub_date.year)
        self.assertEquals(only_news.pub_date.hour, news.pub_date.hour)
        self.assertEquals(only_news.pub_date.minute, news.pub_date.minute)
        self.assertEquals(only_news.pub_date.second, news.pub_date.second)
        self.assertEquals(only_news.category.name, 'Экономика')
        self.assertEquals(only_news.category.description, 'Новости экономики')

class AdminTest(BaseAcceptanceTest):
    fixtures = ['user.json']

    def test_login(self):
        #заходим на страницу входа в админку
        response = self.client.get('/admin/', follow=True)

        #проверяем наличие фразы "Имя пользователя" на странице
        self.assertContains(response, 'Имя пользователя', status_code=200)
        
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/admin/')
        self.assertContains(response, 'Выйти', status_code=200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get('/admin/')
        self.assertContains(response, 'Выйти', status_code=200)

        self.client.logout()
        response = self.client.get('/admin/', follow=True)
        self.assertContains(response, 'Имя пользователя', status_code=200)

    def test_create_news(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        self.client.login(username='testuser', password='testpass')

        response = self.client.get('/admin/news/news/add/')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/news/news/add/', {
            'title': 'Моя первая новость',
            'announcement': 'Анонс первой новости',
            'text': 'Плюс текст первой новости',
            'pub_date_0': '2014-10-15',
            'pub_date_1': '15:35:00',
            'category': str(category.id)
            },
            follow=True
            )
        self.assertContains(response, 'успешно добавлен', status_code=200)

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)

    def test_edit_news(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        news = News()
        news.title = 'Моя первая новость'
        news.announcement = 'Анонс первой новости ++'
        news.text = 'Текст первой новости!!!'
        news.pub_date = timezone.now()
        news.category = category
        news.save()

        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post('/admin/news/news/' + str(news.id) + '/', {
            'title': 'Моя вторая новость',
            'announcement': 'Анонс второй новости',
            'text': 'Текст второй новости',
            'pub_date_0': '2014-10-15',
            'pub_date_1': '16:07:00',
            'category': str(category.id)
            },
            follow=True
            )

        self.assertContains(response, 'успешно изменен', status_code=200)

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)
        only_news = all_news[0]
        self.assertEquals(only_news.title, 'Моя вторая новость')
        self.assertEquals(only_news.announcement, 'Анонс второй новости')
        self.assertEquals(only_news.text, 'Текст второй новости')

    def test_delete_new(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        news = News()
        news.title = 'Моя первая новость'
        news.announcement = 'Анонс первой новости ++'
        news.text = 'Текст первой новости!!!'
        news.pub_date = timezone.now()
        news.category = category
        news.save()

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)

        self.client.login(username='testuser', password='testpass')

        response = self.client.post('/admin/news/news/' + str(news.id) + '/delete/', {
            'post':'yes'
            },
            follow=True
            )
        self.assertContains(response, 'успешно удален', status_code=200)

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 0)

    def test_create_category(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get('/admin/news/category/add/')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/news/category/add/', {
            'name': 'Экономика',
            'description': 'новости экономики',
            'slug': 'economy'
            },
            follow=True
            )
        self.assertContains(response, 'успешно добавлен', status_code=200)

        all_category = Category.objects.all()
        self.assertEquals(len(all_category), 1)

    def test_edit_category(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        self.client.login(username='testuser', password='testpass')

        response = self.client.post('/admin/news/category/' + str(category.id) + '/', {
            'name': 'Политика',
            'description': 'Новости политики',
            'slug': 'politics'
            },
            follow=True
            )
        self.assertContains(response, 'успешно изменен', status_code=200)

        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'Политика')
        self.assertEquals(only_category.description, 'Новости политики')

    def test_delete_category(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        self.client.login(username='testuser', password='testpass')

        response = self.client.post('/admin/news/category/' + str(category.id) + '/delete/', {
            'post': 'yes'
            },
            follow=True
            )
        self.assertContains(response, 'успешно удален', status_code=200)
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)


class NewsViewTest(BaseAcceptanceTest):
    def test_index(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        news = News()
        news.title = 'Моя первая новость'
        news.announcement = 'Анонс первой новости'
        news.pub_date = timezone.now()
        news.category = category
        news.save()

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)

        response = self.client.get('/news/')
        self.assertContains(response, news.title, status_code=200)
        self.assertContains(response, news.announcement)
        self.assertContains(response, news.pub_date.year)
        # выдает на англ и сравнивает с русским - не отрабатывает self.assertContains(response, news.pub_date.strftime('%b'))
        self.assertContains(response, news.pub_date.day)
        self.assertContains(response, news.category.name)

    def test_news_page(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        news = News()
        news.title = 'Моя первая новость'
        news.text = 'Текст первой новости'
        news.pub_date = timezone.now()
        news.category = category
        news.save()

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)

        response = self.client.get('/news/' + str(news.id) + '/')
        self.assertContains(response, news.title, status_code=200)
        self.assertContains(response, news.text)
        self.assertContains(response, news.pub_date.year)
        # выдает на англ и сравнивает с русским - не отрабатывает self.assertContains(response, news.pub_date.strftime('%b'))
        self.assertContains(response, news.pub_date.day)
        self.assertContains(response, news.category.name)

    def test_category_page(self):
        category = Category()
        category.name = 'Экономика'
        category.description = 'Новости экономики'
        category.slug = 'economy'
        category.save()

        news = News()
        news.title = 'Моя первая новость'
        news.announcement = 'Анонс первой новости'
        news.pub_date = timezone.now()
        news.category = category
        news.save()

        all_news = News.objects.all()
        self.assertEquals(len(all_news), 1)
        only_news = all_news[0]
        self.assertEquals(only_news, news)

        category_url = news.category.get_absolute_url()
        response = self.client.get(category_url)
        self.assertContains(response, news.category.name, status_code=200)

        #проверяем атрибуты
        self.assertEquals(only_news.title, 'Моя первая новость')
        self.assertEquals(only_news.announcement, 'Анонс первой новости')
        self.assertEquals(only_news.pub_date.day, news.pub_date.day)
        self.assertEquals(only_news.pub_date.year, news.pub_date.year)

class FlatpagesViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        page = FlatPage()
        page.url = '/about/'
        page.title = 'О компании'
        page.content = 'Страница о компании'
        page.save()

        page.sites.add(Site.objects.all()[0])
        page.save()

        all_page = FlatPage.objects.all()
        self.assertEquals(len(all_page), 1)
        only_page = all_page[0]
        self.assertEquals(only_page, page)

        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'О компании')
        self.assertEquals(only_page.content, 'Страница о компании')

        page_url = only_page.get_absolute_url()

        response = self.client.get(page_url)
        self.assertContains(response, 'О компании', status_code=200)
        self.assertContains(response, 'Страница о компании')