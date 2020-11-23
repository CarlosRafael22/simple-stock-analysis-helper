from extractor import YubbExtractor

class TestYubbExtractor:
    def test_get_stock_indicators_should_return_list_of_tuples(self):
        indicators = YubbExtractor.get_stock_indicators('SEER3')
        assert type(indicators) == list
        assert type(indicators[0]) == tuple
    
    def test_get_indicators_from_stocks_should_return_dict_with_stocks_as_keys(self):
        stocks = ['SEER3', 'COGN3']
        indicators_dict = YubbExtractor.get_indicators_from_stocks(stocks)
        assert type(indicators_dict) == dict
        assert list(indicators_dict.keys()) == stocks

    def test_get_tickers_from_page_should_return_list_of_strs(self):
        tickers = YubbExtractor.get_tickers_from_page(1)
        assert len(tickers) > 0
        assert type(tickers[0]) == str

    def test_get_all_tickets_should_return_list_of_strs(self):
        tickers = YubbExtractor.get_all_tickets()
        # There are at least 300 tickers in the Yubb website
        assert len(tickers) > 300
        assert type(tickers[0]) == str