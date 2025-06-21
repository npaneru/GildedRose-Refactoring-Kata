# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_AgedBrie(self):
        items = [Item("Aged Brie", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(11, items[0].quality)

    def test_aged_quality_lt_50(self):
        items = [Item("Aged Brie", 10, 45)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(46, items[0].quality)

    def test_aged_sell_in_lt_0_qual_lt_50(self):
        items = [Item("Aged Brie", -1, 45)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-2, items[0].sell_in)
        self.assertEqual(47, items[0].quality) # 2 increased when sell_in < 0 & qual <50

    def test_aged_sell_in_lt_0_qual_gt_50(self):
        items = [Item("Aged Brie", -1, 55)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-2, items[0].sell_in)
        self.assertEqual(55, items[0].quality)

    def test_aged_sell_in_gt_0_qual_lt_50(self):
        items = [Item("Aged Brie", 3, 45)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(46, items[0].quality) # 2 increased when sell_in < 0 & qual <50

    def test_aged_sell_in_gt_0_qual_gt_50(self):
        items = [Item("Aged Brie", 3, 55)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(55, items[0].quality) # No change when qual > 50

    # Sulfuras no changes
    def test_sulfuras(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(10, items[0].quality)

    def test_backstage_pass_increase(self):
        items = [
            Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        ]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(items[0].quality, 21)  # +1
        self.assertEqual(items[1].quality, 22)  # +2
        self.assertEqual(items[2].quality, 23)  # +3

    def test_backstage_pass_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(items[0].quality, 0) # Special case when sell< 0 & backastage pass reset quality to 0

    def test_normal_case_quality_gt_0_sell_in_lt_0(self):
        items = [Item("normal case", -1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(8, items[0].quality) # -2 less
        self.assertEqual(-2, items[0].sell_in)
        
    def test_normal_case_quality_eq_1_sell_in_lt_0(self):
        items = [Item("normal case", -1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality) # 1 less
        self.assertEqual(-2, items[0].sell_in)

    def test_normal_case_quality_lt_0_sell_in_lt_0(self):
        items = [Item("normal case", -1, -1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].quality) # no change
        self.assertEqual(-2, items[0].sell_in) # less 1

    def test_normal_case_quality_lt_0_sell_in_eq_1(self):
        items = [Item("normal case", 1, -1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].quality)
        self.assertEqual(0, items[0].sell_in)

    def test_normal_case_quality_gt_0_sell_in_eq_1(self):
        items = [Item("normal case", 1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(0, items[0].sell_in)

    def test_normal_case_quality_gt_0_sell_in_gt_1(self):
        items = [Item("normal case", 3, 12)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)
        self.assertEqual(2, items[0].sell_in)


if __name__ == '__main__':
    unittest.main()
