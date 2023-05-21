from fp_method_builder import *
from method_configurator import *
from fp_method import Method_Result

def main():
    filenames = ['./Tests/Python/test1.py','./Tests/Python/test2.py']
    fp_builder = Fingerprint_Method_Builder(filenames)
    config = Method_Configurator(fp_builder)
    res = config.make_method()
    res.print()

main()