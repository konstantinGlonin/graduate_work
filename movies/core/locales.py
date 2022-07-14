import gettext

from core.config import Config

config = Config()

# todo: Нужен план получше может написать свой класс при инициализации загружаем конфиг при обращение к переменным добавляем в конфиг ключи
try:
    cat = gettext.translation('messages', f'{config.base_dir}/translations/')
    _ = cat.gettext
except:
    def _(text: str = ''):
        return text
