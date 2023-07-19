# GreenWizard

*Pet project, написанный на фреймворке Django 4.2 языка Python.*

![Первый экран](img.png)

## Цель проекта

Основной целью перед собой ставил разработку минимально жизнеспособного продукта в сегмменте e-commerce
решений, для того, чтобы отточить скиллы backend разработчика на фреймворке Django.
Фронтенду я не уделял пристальное внимание, но заострил внимание на бэкенд части.

Проект представляет собой интернет-магазин настольных игр, где есть следующие функциональные разделы:
* Каталог
* Блог
* Личный кабинет
* Корзина
* Заказы
* Оплата
* Фронтенд

Получается достаточно большой сайт с большим кол-вом **функциональных** моделуй, т.е. не 
наборы безжизненных html страниц, а отдельные веб-приложения.

Перед тем, как рассказать про все модули, немного расскажу процессе заполнения базы данных 
товарами.

### Создание проекта

Когда пришла идея делать интернет-магазин, я понял, что нужно собрать "нормальное"
кол-во товаров, чтобы разбить их по категориям и тегам, подлючить пагинацию и фильтрацию и т.д.

Мне нужно было быстрое решение, которое я мог бы собрать "на коленках".

Я решил спарсить сайт конкурентов! Не весь, 150 товарных позиций мне хватило.

    for i in range(1, 6):
        base_url = requests.get(f'https://hobbygames.ru/nastolnie?page={i}&parameter_type=0').text
        soup = BeautifulSoup(base_url, 'html.parser')
        div_elements = soup.find_all('div', class_='col-lg-4 col-md-6 col-sm-6 col-xs-12')

        for div in div_elements:
            title = div.find('a', class_='name')['title']
            duration_text = div.find('div', class_='params__item time').get('title')
            age_limit = div.find('div', class_='params__item age').get('title')
            number_of_persons = div.find('div', class_='params__item players').get('title')

Полный код в модуле game_parser/hobby_games)parsing.py

Решая эту задачу, удалось освежить и попрактиковать работу с библиотеками
**requests** & **bs4**, а также использовать **регулярные выражения** и кастомные приемы обработки и форматирования данных.

### Каталог

Чтобы не тратить лишнее время, сразу расскажу о функционале модуля.

1. Деление на категории
2. Деление на теги (с использованием модуля **taggit**)
3. Пагинация
4. Соритровки
5. Фильтры
6. Детальная карточка товара
7. Связанные игры
8. Поиск (на основе триграммного сходства)

![Пагинация](img_1.png)

Примеры кода:

    # часть кода для функции поиска    
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Game.objects.annotate(
                    similarity=TrigramSimilarity("title", query),
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )

-------------
    # представление детальной страницы товара
    class GameDetail(DetailView):
    template_name = "catalog/products/detail.html"
    model = Game
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        context["game"] = game
        context["cart_product_form"] = CartAddProductForm()
        game.do_number_of_views_plus()
        return context

В коде, работая с представлениями старался использовать как классы так и функции.

### Блог

Тут следующий функционал:
1. Листинг статей
2. Детальная страница статьи
3. Мини CMS (возможность создавать статьи не из админки)
4. Теги к статьям
5. Комменатрии к статьям

Фишка данного раздела - комментарии.
![Комментарии](img_3.png)

### Личный кабинет



### Дополнительно

Реализовал следующие вещи на сайте:

1. Настроил генерацию динамической карты сайта (sitemap.xml)
2. Прикрутил django-bootstrap5
3. Кастомизировал админку (настроил поля, поиск, фильтры и т.д.)


    # чать кода по генерации sitemap
    class GreenWizardSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        games = Game.objects.filter(availability=True)
        categories = Category.objects.all()
        posts = Post.objects.filter(availability=True)
        tags = Tag.objects.all()
        return list(chain(posts, categories, games, tags))

    def lastmod(self, obj):
        if not isinstance(obj, Tag) and obj.updated_at:
            return obj.updated_at
        return timezone.now().date()