import unittest

from geo2 import gbox_tree


class TestCase(unittest.TestCase):
    def test(self):
        tree = gbox_tree.GBoxTree('province', 1)
        for [lnglat, expected_region_ids] in [
            [[79.86481964805327, 6.917311842223569], ['LK-1']],
            [[80.63664111018507, 7.311872685858744], ['LK-2']],
            [[80.21636619668217, 6.027218412807919], ['LK-3']],
            [[80.01192181056106, 9.662254850528123], ['LK-4']],
            [[81.56060482552991, 7.927743036188908], ['LK-5']],
        ]:
            actual_region_ids = tree.find_regions(lnglat)
            self.assertEqual(expected_region_ids, actual_region_ids)


if __name__ == '__main__':
    unittest.main()
