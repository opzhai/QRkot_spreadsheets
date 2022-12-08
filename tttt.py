from datetime import datetime

FORMAT = "%Y/%m/%d %H:%M:%S"

now_date_time = datetime.now().strftime(FORMAT)
spreadsheet_body = {
        'properties': {'title': None,
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 100}}}]
    }

spreadsheet_body['properties']['title'] = f'Отчет на {now_date_time}'

print(spreadsheet_body)
