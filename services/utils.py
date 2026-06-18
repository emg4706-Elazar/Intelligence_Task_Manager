

def calculate_risk_level(diff, impo):
    risk_level = ""
    if 9 >= diff * 2 + impo >= 0:
        risk_level = 'LOW'
    elif 17 >= diff * 2 + impo >= 10:
        risk_level = 'MEDIUM'
    elif 24 >= diff * 2 + impo >= 18:
        risk_level = 'HIGH'
    else:
        risk_level = 'CRITICAL'
    return risk_level





