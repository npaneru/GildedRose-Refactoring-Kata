# -*- coding: utf-8 -*-
import abc
class ItemUpdater(abc.ABC):

    @abc.abstractmethod
    def update(self):
        pass

    # No init duplication in child classes
    def __init__(self, item):
        self.item = item

    def increase_quality(self):
        self.item.quality = min(50, self.item.quality + 1)

    def reduce_quality(self):
        self.item.quality = max(0, self.item.quality - 1) 

class AgedBrieUpdater(ItemUpdater):
        
    def update(self):
        if self.item.quality < 50:
            self.increase_quality()
        self.item.sell_in = self.item.sell_in - 1
        if self.item.sell_in < 0:
            if self.item.quality < 50:
                self.increase_quality()

class BackstagePassUpdater(ItemUpdater):
        
    def update(self):
        
        self.increase_quality()
        if self.item.sell_in < 11:
            self.increase_quality()
        if self.item.sell_in < 6:
            self.increase_quality()
        self.item.sell_in = self.item.sell_in -1
        if self.item.sell_in < 0:
            self.item.quality = 0

class SulfurasUpdater(ItemUpdater):
    def update(self):
        pass

class NormalItemUpdater(ItemUpdater):
    def update(self):
        if self.item.quality > 0:
            self.reduce_quality()
        self.item.sell_in = self.item.sell_in - 1
        if self.item.sell_in < 0:
            if self.item.quality > 0:
                self.reduce_quality()

class GildedRose(object):

    def __init__(self, items):
        self.items = items


    def get_updater(self, item):
        if item.name == "Aged Brie":
            return AgedBrieUpdater(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater(item)
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater(item)
        else:
            return NormalItemUpdater(item)

    def update_quality(self):
        for item in self.items:
            updater = self.get_updater(item)
            updater.update()

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

