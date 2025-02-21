def get_spn(point_obj, point_apt):
    x = float(point_obj[0])
    y = float(point_obj[1])
    x1 = float(point_apt[0])
    y1 = float(point_apt[1])
    spn_x = max(x1, x) - min(x1, x)
    spn_y = max(y1, y) - min(y1, y)
    spn_x += 0.015
    spn_y += 0.015
    return spn_x, spn_y