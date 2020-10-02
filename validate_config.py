from config import Config


def check_config(config: type(Config)):
    error_message = ''
    if config.PATH_TO_EXCEL_FILE == '':
        error_message += 'Ошибка!\nНе указан путь к файлу для чтения.\nУкажите путь в переменной PATH_TO_EXCEL_FILE в config.py\n'
    if config.PATH_TO_SAVE == '':
        error_message += 'Ошибка!\nНе указан путь к файлу для сохранения.\nУкажите путь в переменной PATH_TO_SAVE в config.py\n'
    if error_message:
        print(error_message)
        return False
    if config.PATH_TO_EXCEL_FILE.__contains__(' ') or config.PATH_TO_SAVE.__contains__(' '):
        error_message += 'Ошибка!\nПуть не может содержать пробела\nПроверьте переменные пути в config.py\n'
    if not (config.PATH_TO_EXCEL_FILE.split('.')[1] == 'xlsx' and config.PATH_TO_SAVE.split('.')[1] == 'xlsx'):
        error_message += 'Ошибка!\nРасширение файлов должно быть ".xlsx"!\nПроверьте переменные пути в config.py\n'
    if error_message:
        print(error_message)
        return False
    else:
        return True