from menu_app.view_subclasses import TemplateViewWithMenu
from menu_app.view_menu_context import get_full_menu_context


class IndexView(TemplateViewWithMenu):
    template_name = 'index.html'
