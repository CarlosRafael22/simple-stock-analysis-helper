from analyser import Analyser
import pytest

@pytest.fixture
def stocks_list():
    return ['SEER3', 'COGN3']

@pytest.fixture
def indicators_dict(stocks_list):
    from extractor import YubbExtractor
    indicators_dict = YubbExtractor.get_indicators_from_stocks(stocks_list)
    return indicators_dict

class TestAnalyser:
    def test_create_dataframe_dict_from_indicators_dict(self, indicators_dict, stocks_list):
        dataframe_dict = Analyser.create_dataframe_dict_from_indicators_dict(indicators_dict)
        assert type(dataframe_dict) == dict
        assert type(dataframe_dict['Ação']) == list
        assert len(dataframe_dict['Ação']) == len(stocks_list)

    def test_get_dataframe_indicators_for_stocks(self, indicators_dict, stocks_list):
        dataframe = Analyser.get_dataframe_indicators_for_stocks(stocks_list)
        assert len(list(dataframe.columns)) == len(indicators_dict[stocks_list[0]])
