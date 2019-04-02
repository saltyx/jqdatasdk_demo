from backtesting.simple_backtesting import SimpleBackTesting
import unittest


class TestBacktesing(unittest.TestCase):

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.simple_backtesting = SimpleBackTesting('000027.XSHE')

    def test_simple_backtesting(self):
        self.simple_backtesting.run()

if __name__ == '__main__':
    unittest.main()
