from sys import argv

from factory import Factory
from list_factory import ListFactory
from div_factory import DivFactory


factory_class_info = {
    'ListFactory': ListFactory,
    'DivFactory': DivFactory,
}


def make(file_name: str, factory: Factory):
    # Blog
    blogs = [
        factory.create_link('Blog 1', 'https://example.com/blog1'),
        factory.create_link('Blog 2', 'https://example.com/blog2'),
        factory.create_link('Blog 3', 'https://example.com/blog3'),
    ]
    blog_tray = factory.create_tray('Blog Site')
    for blog in blogs:
        blog_tray.append(blog)

    # News
    newses = [
        factory.create_link('News 1', 'https://example.com/news1'),
        factory.create_link('News 2', 'https://example.com/news2'),
    ]
    news3 = factory.create_tray('News 3')
    news3.append(factory.create_link(
        'News 3 (US)', 'https://example.com/news3us'))
    news3.append(factory.create_link(
        'News 3 (Japan)', 'https://example.com/news3jp'))
    newses.append(news3)

    news_tray = factory.create_tray('News Site')
    for news in newses:
        news_tray.append(news)

    # Page
    page = factory.create_page('Blog and News', 'Hiroshi Yuki')
    page.append(blog_tray)
    page.append(news_tray)

    page.output(file_name=file_name)


if __name__ == '__main__':
    args = argv
    if len(args) != 3:
        print('Usage: python sample.py filename.html class.name.of.ConcreteFactory')
        print('Example 1: python sample.py list.html ListFactory')
        print('Example 2: python sample.py div.html DivFactory')
        exit()

    _, file_name, class_name = args

    factory = factory_class_info.get(class_name)()
    make(file_name=file_name, factory=factory)
