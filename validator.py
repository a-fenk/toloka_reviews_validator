from openpyxl import load_workbook

from excel_service import read_data_from_workbook, CellData, Colors, write_data_to_sheet
from utils import find_duplicates, tokenize, find_unique, check_for_duplicates, has_stopword
from config import Config


def run_validation():
    print('Получаю данные из excel...')
    try:
        workbook = load_workbook(Config.PATH_TO_EXCEL_FILE)
    except FileNotFoundError:
        return print('Ошибка!\nНе удалось найти файл: ' + Config.PATH_TO_EXCEL_FILE + '\nПроверьте переменную PATH_TO_EXCEL_FILE в config.py')
    data = read_data_from_workbook(workbook=workbook)
    print('Успешно')
    for sheet in data:
        print('Начинаю работу с вкладкой ' + sheet['name'])
        res = []
        for row in sheet['data']:
            print('Обрабатываю строку ' + str(row['row'] - 1) + ' из ' + str(len(sheet['data'])))

            # поиск дубликатов между short_descr и result_gold
            short_descr=row['short_descr'].lower()
            duplicates_short_desc, all_flag = find_duplicates(row['short_descr'], row['result_gold'])
            if all_flag:
                color = Colors.BLUE
            elif duplicates_short_desc:
                color = Colors.WHITE
            else:
                color = Colors.GREY
            for token in duplicates_short_desc:
                short_descr = short_descr.replace(token, token.upper())
            res.append(CellData(
                data=short_descr,
                color=color,
                row=row['row'],
                column='U'
            ))
            # поиск уникальных между result_gold и full_description
            result_gold=row['result_gold'].lower()
            unique_result_gold = find_unique(row['result_gold'], row['full_desc'])
            for token in unique_result_gold:
                result_gold = result_gold.replace(token, token.upper())
            res.append(CellData(
                data=result_gold,
                color=Colors.WHITE if unique_result_gold else Colors.GREY,
                row=row['row'],
                column='V'
            ))
            # определение Dublicate short_desc - Unique words result_gold
            res.append(CellData(
                data=result_gold,
                color=Colors.GREEN if all(
                    elem in duplicates_short_desc for elem in unique_result_gold) and unique_result_gold else Colors.WHITE,
                row=row['row'],
                column='Z'
            ))
            # поиск уникальных между full_description и result_gold
            full_desc = row['full_desc'].lower()
            unique_full_description = find_unique(row['full_desc'], row['result_gold'])
            for token in unique_full_description:
                full_desc = full_desc.replace(token, token.upper())
            if len(unique_full_description) >= 2:
                color = Colors.RED
            elif unique_full_description:
                color = Colors.GREY
            else:
                color = Colors.WHITE
            res.append(CellData(
                data=full_desc,
                color=color,
                row=row['row'],
                column='W'
            ))
            # поиск дублей внутри result_gold
            result_gold = row['result_gold'].lower()
            duplicates_result_gold = check_for_duplicates(row['result_gold'])
            for token in duplicates_result_gold:
                result_gold = result_gold.replace(token, token.upper())
            has_digits = any(char.isdigit() for char in row['result_gold'])
            if duplicates_result_gold and has_digits:
                color = Colors.TURQUOISE
            elif has_digits:
                color = Colors.GREEN
            elif duplicates_result_gold:
                color = Colors.GREY
            else:
                color = Colors.WHITE
            res.append(CellData(
                data=result_gold,
                color=color,
                row=row['row'],
                column='X'
            ))
            # поиск дублей внутри full_desc
            full_desc = row['full_desc'].lower()
            duplicates_full_desc = check_for_duplicates(row['full_desc'])
            for token in duplicates_full_desc:
                full_desc = full_desc.replace(token, token.upper())
            has_digits = any(char.isdigit() for char in row['full_desc'])
            if duplicates_full_desc and has_digits:
                color = Colors.TURQUOISE
            elif has_digits:
                color = Colors.GREEN
            elif duplicates_full_desc:
                color = Colors.GREY
            else:
                color = Colors.WHITE
            res.append(CellData(
                data=full_desc,
                color=color,
                row=row['row'],
                column='Y'
            ))
            # поиск стопслов в result_gold
            if has_stopword(row['result_gold']):
                res.append((CellData(
                    color=Colors.RED,
                    row=row['row'],
                    column='I'
                )))
            # поиск символов в result_gold
            elif any(elem in row['result_gold'] for elem in [' ,', ' .', '  ']):
                res.append((CellData(
                    color=Colors.GREY,
                    row=row['row'],
                    column='I'
                )))
            # поиск стопслов в full_desc
            if has_stopword(row['full_desc']):
                res.append((CellData(
                    color=Colors.RED,
                    row=row['row'],
                    column='D'
                )))
            # поиск символов в full_desc
            elif any(elem in row['full_desc'] for elem in [' ,', ' .', '  ']):
                res.append((CellData(
                    color=Colors.GREY,
                    row=row['row'],
                    column='D'
                )))
        print('Сохраняю данные в ' + Config.PATH_TO_SAVE)
        write_data_to_sheet(
            workbook=workbook,
            sheet_name=sheet['name'],
            data=res
        ).save(Config.PATH_TO_SAVE)
        print('Cохранение успешно\nРабота завершена!')
