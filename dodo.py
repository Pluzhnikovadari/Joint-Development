"""Инструмент для атвоматизации."""
from doit.tools import create_folder
import glob


def task_pot():
    """Пересоздать шаблон .pot ."""
    return {'actions': ['pybabel extract -o messages.pot Games'],
            'file_dep': glob.glob('Games/*.py'),
            'targets': ['messages.pot'], }


def task_po():
    """Обновить перевод."""
    return {'actions': ['pybabel update -D messages -d po -i messages.pot'],
            'file_dep': ['messages.pot'],
            'targets': ['po/ru/LC_MESSAGES/messages.po'], }


def task_mo():
    """Скомпилировать перевод."""
    return {'actions': [(create_folder,
                        ['Games/ru/LC_MESSAGES']),
                        'pybabel compile -D messages -l ru -i po/ru/LC_MESSAGES/messages.po -d Games'],
            'file_dep': ['po/ru/LC_MESSAGES/messages.po'],
            'targets': ['Games/ru/LC_MESSAGES/messages.mo'], }