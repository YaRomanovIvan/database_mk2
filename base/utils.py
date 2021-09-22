import datetime
import os
from openpyxl import load_workbook


def calculate_component(amount_trk, amount_eis, amount_vts, amount):
    spent_eis = 0
    spent_trk = 0
    spent_vts = 0
    result = {}
    while amount_trk > 0 and amount > 0:
        amount -= 1
        amount_trk -= 1
        spent_trk += 1
    result["amount_trk"] = amount_trk
    result["spent_trk"] = spent_trk

    while amount_eis > 0 and amount > 0:
        amount -= 1
        amount_eis -= 1
        spent_eis += 1
    result["amount_eis"] = amount_eis
    result["spent_eis"] = spent_eis

    while amount_vts > 0 and amount > 0:
        amount -= 1
        amount_vts -= 1
        spent_vts += 1
    result["amount_vts"] = amount_vts
    result["spent_vts"] = spent_vts
    result["amount"] = amount
    return result


def create_statement(block, cleaned_data):
    path_template = os.path.join(
        os.getcwd(), "base/Statement/Defect.xlsx"
    )
    wb = load_workbook(filename=path_template)
    dest_filename = (
        f"{block.number_block}_{block.serial_number}_{block.name_block}_{block.region}.xlsx"
    )
    sheet = wb["Лист1"]
    sheet["B5"].value = block.number_block
    sheet["D5"].value = block.date_repair
    sheet["A17"].value = str(block.name_block)
    sheet["I20"].value = block.serial_number
    sheet["C20"].value = str(block.region)
    sheet["B26"].value = cleaned_data['defect_1']
    sheet["B28"].value = cleaned_data['defect_2']
    sheet["B30"].value = cleaned_data['defect_3']
    sheet["C47"].value = cleaned_data['result']
    path_save = os.path.join(
        os.getcwd(),
        "base/Statement/Defects/{}".format(
            dest_filename.replace("/", "")
        ),
    )
    wb.save(path_save)
