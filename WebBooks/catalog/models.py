from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, 
                            help_text="Введите жанр книги",
                            verbose_name="Жанр книги")
    objects = models.Manager()

    def __str__(self):
        return str(self.name)


class Language(models.Model):
    name = models.CharField(max_length=20, 
                            help_text="Введите язык книги",
                            verbose_name="Язык книги")
    objects = models.Manager()

    def __str__(self):
        return str(self.name)


class Author(models.Model):
    first_name = models.CharField(max_length=100,
                                  help_text="Введите имя автора",
                                  verbose_name="Имя автора")
    last_name = models.CharField(max_length=100,
                                 help_text="Введите фамилию автора",
                                 verbose_name="Фамилия автора")
    date_of_birth = models.DateField(help_text="Введите дату рождения",
                                     verbose_name="Дата рождения",
                                     null=True, blank=True) #blank fild может быть пустым
    date_of_death = models.DateTimeField(help_text="Введите дату смерти",
                                         verbose_name="Дата смерти",
                                         null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=200, 
                             help_text="Введите название книги",
                             verbose_name="Название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text="Выберите жанр для книги",
                              verbose_name="Жанр книги")
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text="Выберите язык книги",
                                 verbose_name="Язык книги")
    author = models.ManyToManyField('Author', 
                                    help_text="Выберите автора книги",
                                    verbose_name="Автор книги")
    summary = models.TextField(max_length=1000,
                               help_text="Введите описание текста",
                               verbose_name="Описание текста")
    isbn = models.CharField(max_length=13,
                            help_text="Должно содержать 13 символов",
                            verbose_name="ISBN книги")
    objects = models.Manager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class Status(models.Model):
    name = models.CharField(max_length=20,
                            help_text="Введите статус экземпляра книги",
                            verbose_name="Статус экземпляра книги")
    objects = models.Manager()

    def __str__(self):
        return str(self.name)


class BookInstance(models.Model):
    book = models.ForeignKey('Book',
                             on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Введите инвентарный номер книги",
                               verbose_name="Инвентарный номер книги")
    imprint = models.CharField(max_length=200,
                               help_text="Введите издательство и год выпуска",
                               verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                                 null=True,
                                 help_text="Изменить состояние книги",
                                 verbose_name="Статус экземпляра книги")
    due_back = models.DateField(null=True, blank=True,
                                help_text="Введите конец срока статуса",
                                verbose_name="Дата окончания статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Заказчик",
                                 help_text='Выберите заказчика книги')
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
