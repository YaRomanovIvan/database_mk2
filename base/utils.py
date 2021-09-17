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
