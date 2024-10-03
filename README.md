# **TLT_PRO_test**

## Описание проекта

Проект представляет собой пример Django-приложения с кастомными моделями и менеджерами для управления продуктами и их атрибутами. Основная цель проекта — продемонстрировать использование кастомного поля `CustomForeignKey` и связанного с ним менеджера `CustomRelatedManager` для генерации уникальных продуктов.

## Установка и настройка

### 1. Клонирование репозитория

Клонируйте репозиторий на свою локальную машину:

```bash
git clone <URL репозитория>
cd TLT_PRO_test
```

### 2. Создание виртуального окружения

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv/Scripts/activate     # Windows
```

### 3. Установка зависимостей

Установите необходимые зависимости из файла `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Выполнение миграций

Выполните миграции для настройки базы данных:

```bash
python manage.py migrate
```

### 5. Запуск сервера разработки

После успешной установки и миграций вы можете запустить сервер разработки:

```bash
python manage.py runserver
```

## Тестирование

Для запуска тестов используйте следующую команду:

```bash
python manage.py test
```

### Пример теста

В проекте реализован кастомный тест для проверки генерации уникальных продуктов:

```python
class UniqueProductTests(TestCase):
    def setUp(self):
        self.attr = Attr.objects.create(name="Color")
        self.product = Product.objects.create(name="Some Product")
        ProductAttr.objects.create(attr=self.attr, product=self.product, value="Green")

    def test_generate_method(self):
        self.product.unique_products.generate(self.product)
        unique_products = self.product.unique_products.all()
        self.assertEqual(unique_products.count(), 1)
        self.assertEqual(unique_products.first().attr, ProductAttr.objects.filter(product=self.product, attr=self.attr).first())
```

## Структура проекта

- `models.py` — содержит описание моделей, включая кастомный `CustomForeignKey` и кастомный менеджер.
- `tests.py` — содержит тесты для проверки работы кастомных моделей и методов.
- `README.md` — файл с документацией.

## Используемые технологии

- **Python 3.10+**
- **Django 4.0+**
- **SQLite** (по умолчанию для тестов)

## Описание основных компонентов

### Модели

1. **Attr** — модель для описания атрибута продукта.
2. **Product** — основная модель продукта, которая содержит название продукта и связь с атрибутами через модель `ProductAttr`.
3. **ProductAttr** — промежуточная модель для связывания продукта и его атрибутов, а также указания значения атрибута.
4. **UniqueProduct** — модель уникального продукта, который связывает продукт и конкретный атрибут через кастомное поле `CustomForeignKey`.

### Менеджеры

- **CustomRelatedManager** — кастомный менеджер для генерации уникальных продуктов на основе атрибутов продукта.

### Кастомные поля

- **CustomForeignKey** — кастомное поле для создания связи между моделями с использованием кастомного менеджера.

## Об авторе:
Леонид Агалаков - python backend developer.
`https://github.com/Leonid-Agalakov-89`
