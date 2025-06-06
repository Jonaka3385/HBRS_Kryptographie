from ak2.ecc.Points import PointXY, PointXYZ
from ak2.ecc.Weierstrass import WeierstrassCurve


class GlobalDefs:
    xyz_neutral: PointXYZ
    xy_neutral: PointXY

    def __init__(self):
        tmp = WeierstrassCurve(0, 0, 0)
        self.xyz_neutral = PointXYZ(0, 1, 0, tmp)
        self.xy_neutral = PointXY(0, 0, tmp)
        self.xy_neutral.neutral = True
