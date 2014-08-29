from pyrake.item import Item, Field

class IsBullshitItem(Item):
    title = Field()
    author = Field()
    tag = Field()
    date = Field()
    link = Field()