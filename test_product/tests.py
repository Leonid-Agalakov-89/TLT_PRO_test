from django.test import TestCase
from test_product.models import (CustomRelatedManager,
                                 Attr,
                                 Product,
                                 ProductAttr,
                                 UniqueProduct)


class CustomRelatedManagerTests(TestCase):
    """
    Тесты для кастомного менеджера CustomRelatedManager, проверяющие его работу
    и корректность метода generate.
    """

    def setUp(self):
        """
        Подготавливает данные для тестов. Создает экземпляры моделей
        Product, Attr и ProductAttr для использования в тестах.
        """
        self.product = Product.objects.create(name="Test Product")  # Создаем продукт для тестов.
        self.attr = Attr.objects.create(name="Test Attr")  # Создаем атрибут для тестов.
        self.product_attr = ProductAttr.objects.create(product=self.product, attr=self.attr, value="Test Value")  # Создаем связь между продуктом и атрибутом.

    def test_generate_method(self):
        """
        Проверяет работу метода generate кастомного менеджера CustomRelatedManager.
        Метод должен создать объект UniqueProduct для текущего экземпляра Product.
        """
        manager = CustomRelatedManager().for_instance(self.product, 'product')  # Инициализируем кастомный менеджер для текущего продукта.
        manager.generate()  # Выполняем метод generate для создания объектов UniqueProduct.
        self.assertEqual(UniqueProduct.objects.count(), 1)  # Проверяем, что создан один объект UniqueProduct.

    def test_all_method(self):
        """
        Проверяет работу метода all кастомного менеджера CustomRelatedManager.
        """
        # Создаем объект UniqueProduct
        UniqueProduct.objects.create(product=self.product, attr=self.product_attr)
        manager = CustomRelatedManager().for_instance(self.product, ProductAttr._meta.get_field('product'))
        related_objects = manager.all()
        self.assertEqual(related_objects.count(), 1)  # Ожидаем один связанный объект
        self.assertEqual(related_objects.first().product, self.product)
        self.assertEqual(related_objects.first().attr, self.product_attr)
