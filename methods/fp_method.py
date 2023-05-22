class FpMethodResult():
    clone_parts_1: list    # части с заимствованиями из первого файла
    clone_parts_2: list    # части с заимствованиями из второго файла
    clone_pct: float       # процент заимствований

    def __init__(self, cl_pt1, cl_pt2, clp_pct) -> None:
        self.clone_parts_1 = cl_pt1
        self.clone_parts_2 = cl_pt2
        self.clone_pct = clp_pct

    def print(self) -> None:
        print(self.clone_parts_1)
        print(self.clone_parts_2)
        print(self.clone_pct)
