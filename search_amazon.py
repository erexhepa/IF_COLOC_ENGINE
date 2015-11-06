__author__ = 'eltonr'

from amazonproduct import API
AMAZON_ACCESS_KEY = 'AKIAIJHODJ2HNM3BOIZQ'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG  = 'curieinsti-21'

import bottlenose
amazon = bottlenose.Amazon("AMAZON_ACCESS_KEY", "AMAZON_SECRET_KEY")
response = amazon.ItemSearch(ItemId="1429216220", ResponseGroup="Images",
    SearchIndex="Books", IdType="ISBN")


print 'END'