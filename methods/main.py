from fp_method_builder import FingerprintMethodBuilder
from method_configurator import MethodConfigurator


def main():
    filenames = ['./Tests/Python/test6.py', './Tests/Python/test7.py']
    fp_builder = FingerprintMethodBuilder(filenames)
    config = MethodConfigurator(fp_builder)
    res = config.make_method()
    res.print()


main()
