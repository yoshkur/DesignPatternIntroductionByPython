from factory import (
    Factory,
    Link,
    Page,
    Tray,
)


class DivLink(Link):
    def make_html(self):
        return f'<div class="LINK"><a href="{self.url}">{self.caption}</a></div>\n'


class DivTray(Tray):
    def make_html(self):
        str_list = [
            '<p><b>',
            self.caption,
            '</b></p>\n',
            '<div class=\"TRAY\">',
        ]
        for item in self.tray:
            str_list.append(item.make_html())
        str_list.append('</div>\n')
        return ''.join(str_list)


class DivPage(Page):
    def make_html(self):
        str_list = [
            '<!DOCTYPE html>\n',
            '<html><head><title>',
            self.title,
            '</title><style>\n',
            'div.TRAY { padding:0.5em; margin-left:5em; border:1px solid black; }\n',
            'div.LINK { padding:0.5em; background-color: lightgray; }\n',
            '</style></head><body>\n',
            '<h1>',
            self.title,
            '</h1>\n',
        ]
        for item in self.content:
            str_list.append(item.make_html())
        str_list.extend([
            '<hr><address>',
            self.author,
            '</address>\n',
            '</body></html>\n',
        ])
        return ''.join(str_list)


class DivFactory(Factory):
    def create_link(self, caption, url):
        return DivLink(caption=caption, url=url)

    def create_tray(self, caption):
        return DivTray(caption=caption)

    def create_page(self, title, author):
        return DivPage(title=title, author=author)
