from fp_method_builder import *
from method_configurator import *

def main():
    filenames = ['test1.py','test2.py']
    fp_builder = Fingerprint_Method_Builder(filenames)
    config = Method_Configurator(fp_builder)
    config.make_method()

main()