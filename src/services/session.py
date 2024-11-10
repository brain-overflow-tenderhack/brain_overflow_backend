from src.utils import Parameters, SessionData
import requests
from fuzzywuzzy import fuzz
from json import loads
from src.utils import WordExtractor, PdfExtractor
import os


class SessionService:
    DOMEN1 = "https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId="
    DOMEN2 = "https://zakupki.mos.ru/newapi/api/Auction/GetAuctionItemAdditionalInfo?itemId="
    DOMEN3 = "https://zakupki.mos.ru/newapi/api/FileStorage/Download?id="

    def __init__(self, link, options: Parameters = Parameters()):
        self.id = link
        self.options = options
        self.session_data = self.get_session_data()
        self.files = self.__get_files()

    def __get_files(self):
        return self.session_data["files"]

    def check_files(self):
        docx_file = {}
        for file in self.files:
            if "docx" in file["name"].lower():
                docx_file = file
                if "тз" in file["name"].lower() or "техническ" in file["name"].lower():
                    return file
        return docx_file

    def get_session_data(self):
        return loads(requests.get(SessionService.DOMEN1 + self.id).text)

    def get_data(self):
        data = self.session_data

        title = data["name"].lower()
        is_license_needed = data["isLicenseProduction"]
        license_files = data["licenseFiles"]
        is_guarantee_needed = data["isContractGuaranteeRequired"]
        technical_specification = [{"Название": item["name"].lower(),
                                    "Количество": str(int(item["currentValue"])),
                                    # "Стоимость": item["costPerUnit"],
                                    "Характеристики": "\n".join([f"{i["name"].lower()} - {i["value"].lower()}"
                                                                 for i in
                                                                 loads(requests.get(
                                                                     SessionService.DOMEN2 + str(item['id'])).text)[
                                                                     'characteristics']])}
                                   for item in data["items"]]

        return SessionData(title=title, is_license_needed=is_license_needed,
                           is_guarantee_needed=is_guarantee_needed,
                           license_files=license_files, technical_specification=technical_specification)

    def analise(self, session_data: SessionData, options: Parameters, docx_data: SessionData, pdf_data: SessionData = None):
        result = {}
        for option, value in self.options:
            if value:
                if option == "is_license_needed" and not session_data.license_files:
                    # Переписать на Exception или определённый HTTP-ответ.
                    # Но иметь в виду, что лучше продолжать работу функции, чтобы перечислить все найденные ошибки.
                    print("Рекомендуется снятие с публикации. Не хватает документов о лицензии")
                    result[option] = "Рекомендуется снятие с публикации. Не хватает документов о лицензии"
                    continue

                attr1 = getattr(session_data, option)
                attr2 = getattr(docx_data, option)

                if attr1 == attr2:
                    # Полное соответствие, чекаем дальше
                    result[option] = "Полное соответствие"
                    print("Полное соответствие")
                    continue

                # print(attr1)
                # print(attr2)
                a = fuzz.ratio(attr1, attr2)
                # Берём b, как основую метрику, так как она смотрит вхождение слов из первого во второе.
                # avg чисто немного поднять шансы попадания
                b = fuzz.partial_ratio(attr1, attr2)
                c = fuzz.token_sort_ratio(attr1, attr2)
                d = fuzz.token_set_ratio(attr1, attr2)

                avg = (a + b + c + d) // 4
                if b < 80 and avg < 60:
                    print(f"Несоответствие по полю {option}")
                    result[option] = "Несоответствие по полю"
                else:
                    print(f"Неполное соответствие поля {option}, процент соотношения - {b} %")
                    result[option] = f"Неполное соответствие поля, процент соотношения - {b} %"
                # print("ratio:", fuzz.ratio(attr1, attr2))
                # print("partial_ratio:", fuzz.partial_ratio(attr1, attr2))
                # print("token_sort:", fuzz.token_sort_ratio(attr1, attr2))
                # print("token_set:", fuzz.token_set_ratio(attr1, attr2))
                print()

        return result

    def checkout(self):
        file = self.check_files()
        if not file:
            checkout_result = {"title": "Нет документов"}
            return checkout_result
        a = requests.get(f"{SessionService.DOMEN3}{file['id']}")
        filepath = f"../media/{file['name']}"
        with open(filepath, "wb") as f:
            f.write(a.content)

        file_data = WordExtractor(filepath, self.options).parse()

        os.remove(filepath)
        checkout_result = self.analise(self.get_data(), self.options, file_data)
        return checkout_result

# SessionService = _SessionService()
