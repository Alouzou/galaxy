def transform(self, x, y):
    return self.tranfsorm_perspective(x, y)
    # return self.tranfsorm_2D(x, y)


def tranfsorm_2D(self, x, y):
    return int(x), int(y)


def tranfsorm_perspective(self, x, y):
    # TO DO
    lin_y = y * self.perspective_point_y / self.height
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y
    factor_y = diff_y / self.perspective_point_y
    factor_y = pow(factor_y, 4)

    offset_x = diff_x * factor_y

    tr_x = self.perspective_point_x + offset_x
    tr_y = self.perspective_point_y - factor_y * self.perspective_point_y
    return int(tr_x), int(tr_y)