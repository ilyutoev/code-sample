from django.db import models


class Category(models.Model):
    name = models.CharField('Название',max_length=100)
    description = models.TextField('Описание')
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    announcement = models.CharField('Анонс',max_length=255)
    text = models.TextField('Текст новости')
    pub_date = models.DateTimeField('Дата публикации')
    category = models.ForeignKey(Category, null=True, default=None)
    photo = models.ImageField(upload_to = 'news/%Y/%m/%d', null=True, default=None, max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
