from django.db import models
from datetime import date
from django.utils.text import slugify
from transliterate import translit


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название страны")
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация и создание slug
            translit_name = translit(self.name, 'ru', reversed=True)
            base_slug = slugify(translit_name)

            # Проверка уникальности slug среди всех Country, а не Star
            slug = base_slug
            n = 1
            while Country.objects.filter(slug=slug).exists():  # Исправлено: Country вместо Star
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация и создание slug
            translit_name = translit(self.title, 'ru', reversed=True)
            base_slug = slugify(translit_name)

            # Проверка уникальности slug среди всех Category, а не Star
            slug = base_slug
            n = 1
            while Category.objects.filter(slug=slug).exists():  # Исправлено: Category вместо Star
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Star(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя знаменитости")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", default=1)
    birth_date = models.DateField(verbose_name="Дата рождения")
    death_date = models.DateField(
        verbose_name="Дата смерти",
        null=True,
        blank=True,
        help_text='Оставьте пустым, если знаменитость жива'
    )
    content = models.TextField(verbose_name="Описание")
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    @property
    def is_alive(self):
        """Возвращает True, если знаменитость жива (death_date не установлен)."""
        return self.death_date is None

    def get_age(self):
        """Вычисляет возраст звезды на основе даты рождения (и даты смерти, если есть)."""
        reference_date = date.today() if self.is_alive else self.death_date
        age = reference_date.year - self.birth_date.year

        # Корректировка, если день рождения еще не наступил в этом году
        if (reference_date.month, reference_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return max(0, age)  # Возвращаем 0, если возраст отрицательный

    def get_age_with_correct_word(self):
        """Возвращает возраст с правильным склонением слова 'год'."""
        age = self.get_age()
        last_digit = age % 10
        last_two_digits = age % 100

        if 11 <= last_two_digits <= 14:
            return f"{age} лет"
        if last_digit == 1:
            return f"{age} год"
        elif 2 <= last_digit <= 4:
            return f"{age} года"
        else:
            return f"{age} лет"

    def get_lifespan(self):
        """Возвращает строку с годами жизни в формате 'ГГГГ-ГГГГ' или 'ГГГГ-настоящее время'."""
        birth_year = self.birth_date.year
        if self.is_alive:
            return f"{birth_year} - настоящее время"
        return f"{birth_year}-{self.death_date.year}"

    def get_categories_display(self):
        """Возвращает строку с категориями через запятую"""
        return self.category.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация и создание slug
            translit_name = translit(self.name, 'ru', reversed=True)
            base_slug = slugify(translit_name)

            # Проверка уникальности slug
            slug = base_slug
            n = 1
            while Star.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Знаменитость'
        verbose_name_plural = 'Знаменитости'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]