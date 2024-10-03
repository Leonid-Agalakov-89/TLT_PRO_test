from django.db import models
from django.db.models.fields.related import (ForeignKey,
                                             ReverseManyToOneDescriptor)


class CustomRelatedManager(models.Manager):
    """
    Кастомный менеджер для управления связанными объектами,
    предоставляющий методы для получения всех связанных объектов
    и создания новых объектов на основе текущего экземпляра.
    """

    def __init__(self, instance=None, field=None, *args, **kwargs):
        """
        Инициализация кастомного менеджера с экземпляром модели
        и полем ForeignKey, которое используется для связи моделей.
        """
        super().__init__(*args, **kwargs)
        self.instance = instance  # Экземпляр модели, связанный с данным менеджером.
        self.field = field  # Поле ForeignKey, которое используется для связи моделей.

    def for_instance(self, instance, field):
        """
        Устанавливает текущий экземпляр модели и поле ForeignKey
        для использования в методах менеджера.

        :param instance: Экземпляр модели, с которым связаны объекты.
        :param field: Поле ForeignKey, используемое для фильтрации объектов.
        :return: Возвращает текущий экземпляр CustomRelatedManager.
        """
        self.instance = instance
        self.field = field
        return self

    def all(self):
        """
        Возвращает все связанные объекты, фильтруя по текущему
        экземпляру модели. Если экземпляр не установлен, возвращает
        все объекты без фильтрации.

        :return: QuerySet всех связанных объектов.
        """
        if self.instance is None:
            return super().all()  # Если экземпляр не установлен, возвращаем все объекты.
        return super().filter(**{self.field.name: self.instance})  # Фильтруем объекты по полю ForeignKey.

    def generate(self):
        """
        Создает объекты UniqueProduct для текущего экземпляра Product,
        основываясь на связанных атрибутах.

        :raises ValueError: Если экземпляр не установлен.
        """
        if self.instance is None:
            raise ValueError("Instance not set")  # Выбрасываем исключение, если экземпляр не установлен.
        attrs = ProductAttr.objects.filter(
            product=self.instance)  # Находим все связанные атрибуты.
        for attr in attrs:
            UniqueProduct.objects.create(
                product=self.instance,
                attr=attr)  # Создаем объекты UniqueProduct.


class CustomReverseManyToOneDescriptor(ReverseManyToOneDescriptor):
    """
    Кастомный дескриптор для управления доступом к связанным объектам
    через CustomRelatedManager.
    """

    def __get__(self, instance, cls=None):
        """
        Возвращает кастомный менеджер CustomRelatedManager, инициализированный
        текущим экземпляром модели и полем ForeignKey.

        :param instance: Экземпляр модели, к которому осуществляется доступ.
        :param cls: Класс модели (не используется).
        :return: CustomRelatedManager для текущего экземпляра и поля.
        """
        if instance is None:
            return self  # Если экземпляр не установлен, возвращаем сам дескриптор.
        return CustomRelatedManager().for_instance(
            instance, self.field)  # Создаем и возвращаем кастомный менеджер.


class CustomForeignKey(ForeignKey):
    """
    Кастомный ForeignKey, который использует кастомный дескриптор
    для доступа к связанным объектам.
    """

    related_accessor_class = CustomReverseManyToOneDescriptor  # Указываем кастомный дескриптор для доступа.

    def __init__(self, to, **kwargs):
        """
        Инициализирует кастомный ForeignKey, передавая параметры родительскому
        классу ForeignKey.

        :param to: Модель, к которой осуществляется связь.
        :param kwargs: Дополнительные параметры для ForeignKey.
        """
        super().__init__(to, **kwargs)  # Инициализируем родительский класс.


class Attr(models.Model):
    """
    Модель для хранения атрибутов, таких как цвет, размер и т.д.
    """

    name = models.CharField(
        max_length=50
    )  # Поле для хранения имени атрибута.

    def __str__(self):
        """
        Возвращает строковое представление атрибута.

        :return: Строковое представление имени атрибута.
        """
        return self.name


class ProductAttr(models.Model):
    """
    Модель для хранения связи между продуктом и атрибутом,
    включая значение атрибута для конкретного продукта.
    """

    attr = models.ForeignKey(
        "Attr",
        on_delete=models.CASCADE
    )  # Связь с моделью Attr.
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE
    )  # Связь с моделью Product.
    value = models.CharField(
        max_length=100
    )  # Поле для хранения значения атрибута.


class Product(models.Model):
    """
    Модель для хранения продуктов. Продукты могут иметь множество
    атрибутов через промежуточную модель ProductAttr.
    """

    name = models.CharField(
        max_length=100
    )  # Поле для хранения имени продукта.
    attrs = models.ManyToManyField(
        "Attr", through="ProductAttr"
    )  # Связь многие ко многим через промежуточную модель ProductAttr.

    def __str__(self):
        """
        Возвращает строковое представление продукта.

        :return: Строковое представление имени продукта.
        """
        return self.name


class UniqueProduct(models.Model):
    """
    Модель для хранения уникальных продуктов с конкретными атрибутами.
    """

    product = CustomForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='unique_products'
    )  # Кастомный ForeignKey для связи с Product.
    attr = models.ForeignKey(
        ProductAttr,
        on_delete=models.PROTECT
    )  # Связь с моделью ProductAttr.

    objects = models.Manager()  # Стандартный менеджер для создания объектов.
