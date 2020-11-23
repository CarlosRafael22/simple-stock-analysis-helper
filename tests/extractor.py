from extractor import YubbExtractor

class TestYubbExtractor:
    def test_get_stock_indicators(self):
        Extractor = YubbExtractor()
        indicators = Extractor.get_stock_indicators('SEER3')
        assert type(indicators) == list
        assert type(indicators[0]) == tuple
    
    def test_get_indicators_from_stocks(self):
        Extractor = YubbExtractor()
        stocks = ['SEER3', 'COGN3']
        indicators_dict = Extractor.get_indicators_from_stocks(stocks)
        assert type(indicators_dict) == dict
        assert list(indicators_dict.keys()) == stocks