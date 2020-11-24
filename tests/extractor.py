from extractor import YubbExtractor
import pytest


@pytest.fixture
def tickers_list():
    return ['SEER3', 'COGN3', 'YDUQ3']


class TestYubbExtractor:
    def test_get_stock_indicators_should_return_list_of_tuples(self):
        indicators = YubbExtractor.get_stock_indicators('SEER3')
        assert type(indicators) == list
        assert type(indicators[0]) == tuple
    
    def test_get_indicators_from_stocks_should_return_dict_with_stocks_as_keys(self, tickers_list):
        indicators_dict = YubbExtractor.get_indicators_from_stocks(tickers_list)
        assert type(indicators_dict) == dict
        assert list(indicators_dict.keys()) == tickers_list

    def test_get_tickers_from_page_should_return_list_of_strs(self):
        tickers = YubbExtractor.get_tickers_from_page(1)
        assert len(tickers) > 0
        assert type(tickers[0]) == str

    def test_get_all_tickers_should_return_list_of_strs(self):
        tickers = YubbExtractor.get_all_tickers()
        # There are at least 300 tickers in the Yubb website
        assert len(tickers) > 300
        assert type(tickers[0]) == str

        # Also saving to not need to retrieve them all again
        YubbExtractor.save_list_to_file(tickers, 'yubb_tickers.txt')
    
    def test_should_save_list_to_file(self, tickers_list):
        import os.path

        filename = 'tickers.txt'
        try:
            os.remove(filename)
        except Exception:
            pass

        YubbExtractor.save_list_to_file(tickers_list, filename)
        assert os.path.exists(filename)

    def test_should_get_list_from_file(self, tickers_list):
        returned_tickers_list = YubbExtractor.get_list_from_file('tickers.txt')
        assert returned_tickers_list == tickers_list