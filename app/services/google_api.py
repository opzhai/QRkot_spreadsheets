from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
RANGE_UPDATE = 'A1:E400'
SPREADSHEET_BODY = {
    'properties': {'title': None, 'locale': 'ru_RU'},
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {'rowCount': 100, 'columnCount': 100}
        }
    }]
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    SPREADSHEET_BODY['properties']['title'] = f'Отчет на {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        closure_period = project.close_date - project.create_date
        new_row = [str(project.name), str(closure_period), str(project.description)]
        table_values.append(new_row)
    table_values = table_values[0:3] + sorted(
        table_values[3:], key=lambda project: project[1]
    )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE_UPDATE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
