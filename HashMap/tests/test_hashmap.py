import pytest
from hash.app_hashmap import HashDictionary
from hash.iloc import IlocException
from hash.ploc import PlocException
from hash.iloc import Iloc
from hash.ploc import Ploc

class TestHashDictionary:

    @pytest.fixture
    def hash_dict(self):
        return HashDictionary()

    @pytest.fixture
    def sample_data(self):
        return {
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
        }

    def test_iloc_valid_index(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        iloc_obj = Iloc(data)

        assert iloc_obj[0] == 1
        assert iloc_obj[1] == 2
        assert iloc_obj[2] == 3

    def test_iloc_invalid_index(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        iloc_obj = Iloc(data)

        with pytest.raises(IlocException, match="Invalid index"):
            value = iloc_obj[5]


    def test_iloc_empty_dict(self):
        data = {}
        iloc_obj = Iloc(data)

        with pytest.raises(IlocException, match="Invalid index"):
            value = iloc_obj[0]

    def test_iloc_negative_index(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        iloc_obj = Iloc(data)

        with pytest.raises(IlocException, match="Invalid index"):
            value = iloc_obj[-1]

    def test_iloc_mixed_types(self):
        data = {1: 'a', 'b': 2, 'c': 3}
        iloc_obj = Iloc(data)

        assert iloc_obj[0] == 'a'
        assert iloc_obj[1] == 2
        assert iloc_obj[2] == 3

    def test_ploc_creation(self, sample_data):
        ploc_instance = Ploc(sample_data)
        assert isinstance(ploc_instance, Ploc)

    def test_ploc_operation(self):
        ploc_instance = Ploc({})
        assert ploc_instance.operation("==", 3, 3)
        assert not ploc_instance.operation("==", 2, 3)
        assert ploc_instance.operation(">", 5, 3)
        assert not ploc_instance.operation(">", 2, 3)


    def test_ploc_condition_check_single_condition(self):
        ploc_instance = Ploc({})
        buf_conditions = [['>', 3]]
        item = 4
        count = 1
        assert ploc_instance.condition_check(buf_conditions, item, count)

    def test_ploc_condition_check_no_match(self):
        ploc_instance = Ploc({})
        buf_conditions = [['>', 3], ['=', 5], ['<', 1]]
        item = [2, 5, 4]
        count = 3
        assert not ploc_instance.condition_check(buf_conditions, item, count)



    def test_initialization(self, hash_dict):
        assert isinstance(hash_dict, HashDictionary)
        assert isinstance(hash_dict.iloc, Iloc)
        assert isinstance(hash_dict.ploc, Ploc)

    def test_set_and_get_item(self, hash_dict):
        hash_dict['key1'] = 'value1'
        assert hash_dict['key1'] == 'value1'

    def test_set_and_get_item_with_ploc(self, hash_dict):
        with pytest.raises(AttributeError):
            hash_dict.ploc.set('key2', 'value2')

    def test_set_and_get_item_with_iloc(self, hash_dict):
        with pytest.raises(AttributeError):
            hash_dict.iloc.set(0, 'value3')


    def test_del_item(self, hash_dict):
        hash_dict['key6'] = 'value6'
        del hash_dict['key6']
        with pytest.raises(KeyError):
            value = hash_dict['key6']

    def test_del_item_with_ploc(self, hash_dict):
        with pytest.raises(AttributeError):
            hash_dict.ploc.set('key7', 'value7')

    def test_del_item_with_iloc(self, hash_dict):
        with pytest.raises(AttributeError):
            hash_dict.iloc.set(1, 'value8')

    def test_iloc(self):
        d = HashDictionary()
        d["value1"] = 1
        d["value2"] = 2
        d["value3"] = 3
        d["1"] = 10
        d["2"] = 20
        d["3"] = 30
        d["1, 5"] = 100
        d["5, 5"] = 200
        d["10, 5"] = 300
        assert d.iloc[0] == 10
        assert d.iloc[2] == 300
        assert d.iloc[5] == 200
        assert d.iloc[8] == 3
        with pytest.raises(IlocException):
            d.iloc[10]

    def test_ploc(self):
        d = HashDictionary()
        d["value1"] = 1
        d["value2"] = 2
        d["value3"] = 3
        d["1"] = 10
        d["2"] = 20
        d["3"] = 30
        d["(1, 5)"] = 100
        d["(5, 5)"] = 200
        d["(10, 5)"] = 300
        d["(1, 5, 3)"] = 400
        d["(5, 5, 4)"] = 500
        d["(10, 5, 5)"] = 600
        assert d.ploc[">=1"] == "{1=10, 2=20, 3=30}"
        assert d.ploc["<3"] == "{1=10, 2=20}"
        assert d.ploc[">0, >0"] == "{(1, 5)=100, (5, 5)=200, (10, 5)=300}"
        assert d.ploc[">=10,     >0"] == "{(10, 5)=300}"
        assert d.ploc["<5, >=5, >=3"] == "{(1, 5, 3)=400}"
        assert d.ploc["<0"] == ""
        assert d.ploc["==1"] == "{1=10}"
        assert d.ploc["<=2"] == "{1=10, 2=20}"
        assert d.ploc["<>1"] == "{2=20, 3=30}"