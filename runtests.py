import sys;
from tests import test_sample
import os.path

tester = test_sample(os.path.abspath(__file__), "runtests")

tester.main(sys.argv[1:])
