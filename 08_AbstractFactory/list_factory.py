from factory import (
    Factory,
    Link,
    Page,
    Tray,
)


class ListLink(Link):
    def make_html(self):
        return f'<li><a href="{self.url}">{self.caption}</a></li>\n'


class ListTray(Tray):
    def make_html(self):
        str_list = [
            '<li>\n',
            self.caption,
            '\n<ul>\n',
        ]
        for item in self.tray:
            str_list.append(item.make_html())
        str_list.extend([
            '</ul>\n',
            '</li>\n',
        ])
        return ''.join(str_list)


class ListPage(Page):
    def make_html(self):
        str_list = [
            '<!DOCTYPE html>\n',
            '<html><head><title>',
            self.title,
            '</title></head>\n',
            '<body>\n',
            '<h1>',
            self.title,
            '</h1>\n',
            '</ul>\n',
        ]
        for item in self.content:
            str_list.append(item.make_html())
        str_list.extend([
            '</ul>\n',
            '<hr><address>',
            self.author,
            '</address>\n',
            '</body></html>\n',
        ])
        return ''.join(str_list)


class ListFactory(Factory):
    def create_link(self, caption, url):
        return ListLink(caption=caption, url=url)

    def create_tray(self, caption):
        return ListTray(caption=caption)

    def create_page(self, title, author):
        return ListPage(title=title, author=author)
