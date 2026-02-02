import logging

import gspread_asyncio
from google.oauth2.service_account import Credentials


class GspreadManager:

    def __init__(self):
        self.agcm = gspread_asyncio.AsyncioGspreadClientManager(self.get_creds())

    @staticmethod
    def get_creds():
        creds = Credentials.from_service_account_file('creds.json')
        return creds.with_scopes([
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        )

    async def get_tm_sheet(self):
        agcm = await self.agcm.authorize()
        sheet = await agcm.open('TMsheet')
        wk: gspread_asyncio.AsyncioGspreadWorksheet = await sheet.get_worksheet(0)
        return wk

    async def get_all_users(self):
        wk = await self.get_tm_sheet()
        data = await wk.col_values(8)
        return data

    async def save_data(self, data: dict):
        wk = await self.get_tm_sheet()
        await wk.append_row(
            [
                data['city'],
                data['event_date'],
                data['name'],
                data['univercity'],
                data['phone'],
                data['date'],
                data['user_name'],
                data['user_id']]
        )

    async def all_data(self):
        wk = await self.get_tm_sheet()
        all_data = await wk.get_all_records()
        logging.info(all_data)
        return all_data
