import os
from openpyxl import load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment

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


def create_statement(block, cleaned_data, date):
    path_template = os.path.join(
        os.getcwd(), "base/Statement/Defect.xlsx"
    )
    wb = load_workbook(filename=path_template)
    dest_filename = (
        f"{block.number_block}_{block.serial_number}_{block.name_block}_{block.region}.xlsx"
    )
    sheet = wb["Лист1"]
    sheet["B5"].value = block.number_block
    sheet["D5"].value = date
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


def create_repair_maker(qs):
    path_template = os.path.join(
        os.getcwd(), "base/Maker/pattern.xlsx"
    )
    wb = load_workbook(filename=path_template)
    sheet = wb["Лист1"]
    cnt = 2
    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
    for record in qs:
        sheet["A" + str(cnt)].value = str(record.block.number_block)
        sheet["B" + str(cnt)].value = str(record.block.name_block)
        sheet["C" + str(cnt)].value = str(record.block.serial_number)
        sheet["D" + str(cnt)].value = str(record.block.region)
        sheet["E" + str(cnt)].value = str(record.maker)
        sheet["F" + str(cnt)].value = record.block.date_add
        sheet["G" + str(cnt)].value = record.date_shipment_maker
        sheet["H" + str(cnt)].value = record.date_add_maker
        sheet["I" + str(cnt)].value = record.maker_status
        cnt += 1
    for i in range(1, len(qs)+2):
        sheet.cell(row=i, column=1).border = thin_border
        sheet.cell(row=i, column=2).border = thin_border
        sheet.cell(row=i, column=3).border = thin_border
        sheet.cell(row=i, column=4).border = thin_border
        sheet.cell(row=i, column=5).border = thin_border
        sheet.cell(row=i, column=6).border = thin_border
        sheet.cell(row=i, column=7).border = thin_border
        sheet.cell(row=i, column=8).border = thin_border
        sheet.cell(row=i, column=9).border = thin_border
    path_save = os.path.join(
        os.getcwd(),
        "base/Maker/repair_maker.xlsx"
    )
    wb.save(path_save)


def create_report_excel(order, date_after, date_before, company):
    unique_invoice_number = list({v['invoice_number']:v for v in order.values('invoice_number', 'invoice_amount')}.values()) # получаем уникальные номера счетов и их сумму
    invoice_order = {}
    all_cnt_component = 0
    all_summ_invoice = 0
    for i in unique_invoice_number:
        cnt_component = order.filter(invoice_number=i['invoice_number']).values('component').count() # считаем количество компонентов в счете
        invoice_order[i['invoice_number']] = [cnt_component, i['invoice_amount']] # словарь с указанием номера счета, количества компонентов в счете и сумма счета
        all_cnt_component += cnt_component
        all_summ_invoice += i['invoice_amount']
    agr = []
    for i in unique_invoice_number:
        agr.append(i['invoice_amount'])
    if agr:
        max_invoice = max(agr)
        min_invoice = min(agr)
        avg_invoice = sum(agr) / len(agr)

    path_template = os.path.join(
        os.getcwd(), "base/Order report/report_order_template.xlsx"
    )
    wb = load_workbook(filename=path_template)
    sheet = wb["Лист1"]
    cnt = 5
    for record in order:
        sheet["B" + str(cnt)].value = str(record.invoice_number)
        sheet["C" + str(cnt)].value = str(record.component.type_component)
        sheet["D" + str(cnt)].value = str(record.component.marking)
        sheet["E" + str(cnt)].value = str(record.amount_commit)
        sheet["B" + str(cnt)].alignment = Alignment(horizontal='center')
        sheet["E" + str(cnt)].alignment = Alignment(horizontal='center')

        cnt += 1
    cnt = 5
    for record in invoice_order:
        sheet["G" + str(cnt)].value = str(record)
        sheet["H" + str(cnt)].value = int(invoice_order[record][0])
        sheet["I" + str(cnt)].value = float(invoice_order[record][1])
        sheet["G" + str(cnt)].alignment = Alignment(horizontal='center')
        sheet["H" + str(cnt)].alignment = Alignment(horizontal='center')
        sheet["I" + str(cnt)].alignment = Alignment(horizontal='center')
        cnt += 1
    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
    for i in range(5, order.count()+5):
        sheet.cell(row=i, column=2).border = thin_border
        sheet.cell(row=i, column=3).border = thin_border
        sheet.cell(row=i, column=4).border = thin_border
        sheet.cell(row=i, column=5).border = thin_border

    for i in range(5, len(invoice_order)+5):
        sheet.cell(row=i, column=7).border = thin_border
        sheet.cell(row=i, column=8).border = thin_border
        sheet.cell(row=i, column=9).border = thin_border
    sheet["L4"].value = str(company)
    sheet["L5"].value = f'{date_after} - {date_before}'
    sheet["L6"].value = int(len(unique_invoice_number))
    sheet["L7"].value = int(all_cnt_component)
    sheet["L8"].value = int(all_summ_invoice)
    sheet["L10"].value = float(min_invoice)
    sheet["L11"].value = float(max_invoice)
    sheet["L12"].value = float(avg_invoice)

    sheet["L4"].alignment = Alignment(horizontal='center')
    sheet["L5"].alignment = Alignment(horizontal='center')
    sheet["L6"].alignment = Alignment(horizontal='center')
    sheet["L7"].alignment = Alignment(horizontal='center')
    sheet["L8"].alignment = Alignment(horizontal='center')
    sheet["L10"].alignment = Alignment(horizontal='center')
    sheet["L11"].alignment = Alignment(horizontal='center')
    sheet["L12"].alignment = Alignment(horizontal='center')

    path_save = os.path.join(
        os.getcwd(),
        "base/Order report/report.xlsx"
    )
    wb.save(path_save)
    
