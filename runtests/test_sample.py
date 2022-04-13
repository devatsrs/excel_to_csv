import unittest


class TestExcel(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')


# print (__name__)

if __name__ == '__main__':
  unittest.main()


#print (_get_fixture('test_excel.xlsx'))