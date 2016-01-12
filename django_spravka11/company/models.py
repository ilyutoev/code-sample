from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime

class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    ico = models.ImageField('Иконка', upload_to = 'company/category', null=True, default=None, blank=True)
    article = models.TextField('Статья', blank=True, null=True, default=None)

    def __str__(self):
        return self.name
        
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'рубрику'
        verbose_name_plural = 'рубрики'

class Company(models.Model):
    name = models.CharField('Название компании', max_length=255)
    website = models.URLField('Адрес сайта', blank=True)
    email = models.EmailField('E-mail', blank=True)
    vkontakte = models.URLField('Страница ВКонтакте', blank=True)
    dateupdate = models.DateField('Дата последнего обновления')
    logo = models.ImageField('Логотип', upload_to = 'uploads/logo', null=True, default=None, blank=True)
    banner = models.ImageField('Рекламный модуль', upload_to = 'uploads/module', null=True, default=None, blank=True)
    keywords = models.CharField('Ключевые слова', blank=True, max_length=255)
    article = models.TextField('Статья о компании', blank=True)
    priority = models.IntegerField('Приоритет', help_text='Приоритет компании в зависимости от купленной рекламы (больше - лучше)', default=1)
    recomendation = models.BooleanField('Рекомендуем', help_text='Вывод на главную страницу в блок "Рекомендуем", бирка "Рекомендуем"', default=False)
    recomendationtext = models.CharField('Текст рекомендации для главной', blank=True, max_length=255)
    vizitka = models.BooleanField('Сайт визитка', default=False)
    img_vizitka = models.ImageField('Изображение для шапки сайта визитки', upload_to = 'uploads/vizitka', null=True, default=None, blank=True, help_text='Ширина картинки 1170 px, высоту регулируйте сами - оптимально от 100-200 px')
    yellow = models.BooleanField('На первое место', help_text='Выделяем желтым и добавляем выоский приоритет', default=False)
    blue = models.BooleanField('На второе место', help_text='Выделяем синим и ставим на второе метос', default=False)
    counter = models.IntegerField('Счетчик посещений', default=1)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'компанию'
        verbose_name_plural = 'компании'

    def category(self):
        temp = Address.objects.filter(company=self)
        temp = Category.objects.filter(address__in=temp).distinct()
        return temp

    def address_count(self):
        return Address.objects.filter(company=self.pk).count()

    def common_company(self):
        temp = Address.objects.filter(company=self)
        temp = Category.objects.filter(address__in=temp).distinct().values_list('id', flat=True)
        return Company.objects.filter(address__category__in=temp).exclude(pk=int(self.pk)).distinct()[:3]

    def page_for_vizitka(self):
        return CompanyPage.objects.filter(company=self, ismemu=True).order_by('-priority')

    def clear_address(self):
        address = Address.objects.filter(company=self)
        try:
            fix_address = []
            for adr in address:
                fix_address.append(adr.address[adr.address.find(',')+1:].strip())
            return fix_address
        except:
            return address

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)

class City(models.Model):
    name = models.CharField('Город', max_length=50)
    priority = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

class Address(models.Model):
    company = models.ForeignKey(Company, verbose_name="компания")
    #список городов как табличка + приоритет для вывода
    city = models.ForeignKey(City, verbose_name="город")
    address = models.CharField('Адрес', max_length=255)
    category = models.ManyToManyField(Category, verbose_name="рубрики")

    #для создания поискового индекса - все связанные рубрики в строку и в индекс
    def get_category(self):
        string = ''
        try:
            for cat in self.category.all():
                string += ' ' + str(cat.name) + ' ' + str(cat.parent.name) + ' ' + str(cat.parent.parent.name)
        except:
            pass
        return string

    def get_timetable_all(self):
        return Timetable.objects.filter(address=self).order_by('day')

    def get_timetable_today(self):
        return Timetable.objects.filter(day=datetime.today().weekday() + 1, address=self)

    def get_phone(self):
        return Phone.objects.filter(address=self).values('number').values_list('number', flat=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес компании'
        verbose_name_plural = 'Адреса компании'

class Phone(models.Model):
    number = models.CharField('Номер телефона', max_length=200)
    address = models.ForeignKey(Address)

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = 'номер телефона компании'
        verbose_name_plural = 'номера телефонов компаний'

class Timetable(models.Model):
    DAY_TYPE = (
        (1, 'Пн'),
        (2, 'Вт'),
        (3, 'Ср'),
        (4, 'Чт'),
        (5, 'Пт'),
        (6, 'Сб'),
        (7, 'Вс'),
        )
    day = models.IntegerField('День недели', choices=DAY_TYPE)
    worktimebegin = models.TimeField('Начало работы', blank=True, null=True, default='00:00:00')
    worktimeend = models.TimeField('Конец работы', blank=True, null=True, default='00:00:00')
    holiday =models.BooleanField('Выходной', default=False)
    lunchtimebegin = models.TimeField('Начало обеда', blank=True, null=True, default='00:00:00')
    lunchtimeend = models.TimeField('Конец обеда', blank=True, null=True, default='00:00:00')
    address = models.ForeignKey(Address)

    class Meta:
        verbose_name = 'Время работы'
        verbose_name_plural = 'Время работы'

    def __str__(self):
        return self.address.address + ' - ' + self.get_day_display()

class CompanyImage(models.Model):
    image = models.ImageField('Изображение', upload_to = 'company/images/%Y/%m/%d', null=True, default=None)
    company = models.ForeignKey(Company, verbose_name="компания")

    def __str__(self):
        return self.company.name
    
    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

class CompanyPage(models.Model):
    company = models.ForeignKey(Company, verbose_name="компания")
    title = models.CharField('Заголовок страницы', max_length=200)
    slug = models.SlugField('Ссылка страницы', help_text='Латинские буквы, нижнее подчеркивание')
    text = models.TextField('Наполнение страницы')
    ismemu = models.BooleanField('Вывести в меню', default=False)
    title_menu = models.CharField('Заголовок для меню', max_length=200, blank=True)
    priority = models.IntegerField('Приоритет в меню', default=0, help_text='Больше - лучше')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Страница сайта визитки'
        verbose_name_plural = 'Страницы сайта визитки'

class CompanyService(models.Model):
    title = models.CharField('Название товара/услуги', max_length=200)
    text = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to = 'company/service/%Y/%m/%d', null=True, default=None)
    company = models.ForeignKey(Company, verbose_name="компания")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'товар/услуга'
        verbose_name_plural = 'товары/услуги'

class CompanyNews(models.Model):
    company = models.ForeignKey(Company, verbose_name="компания")
    title = models.CharField('Заголовок', max_length=200)
    announcement = models.CharField('Анонс',max_length=255)
    text = models.TextField('Текст новости')
    pub_date = models.DateTimeField('Дата публикации')
    photo = models.ImageField(upload_to = 'news/%Y/%m/%d', null=True, default=None, max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'новость компании'
        verbose_name_plural = 'новости компаний'