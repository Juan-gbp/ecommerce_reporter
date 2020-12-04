from redis import Redis
from collector import DailyDeal, update_db, collect_deal, deal_has_changed


# Make sure the redis-server process is running before running tests
def test_empty_db_has_no_values():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    assert r_test.llen('product_name') == 0
    assert r_test.llen('product_price') == 0
    assert r_test.llen('product_sport') == 0


def test_update_db_adds_new_deal():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal = DailyDeal('item', int(1), 'mma')
    update_db(r_test, deal)

    assert r_test.llen('product_name') == 1
    assert r_test.llen('product_price') == 1
    assert r_test.llen('product_sport') == 1

    assert r_test.lindex('product_name', 0).decode().strip() == 'item'
    assert int(r_test.lindex('product_price', 0).decode()) == int(1)
    assert r_test.lindex('product_sport', 0).decode().strip() == 'mma'


def test_first_deal_always_is_changed_deal():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal = DailyDeal('item', int(1), 'bjj')

    assert deal_has_changed(r_test, deal) is True


def test_other_sport_is_always_changed_deal_when_first_of_that_sport():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    bjj_deal = DailyDeal('item', int(1), 'bjj')
    update_db(r_test, bjj_deal)

    mma_deal = DailyDeal('other item', int(5), 'mma')

    assert deal_has_changed(r_test, mma_deal) is True



def test_deal_not_changed_if_same_deal():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal = DailyDeal('item', int(1), 'bjj')
    update_db(r_test, deal)

    assert deal_has_changed(r_test, deal) is False


def test_deal_changed_if_different_deal():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal = DailyDeal('item', int(1), 'mma')
    update_db(r_test, deal)

    new_deal = DailyDeal('different item', int(5), 'mma')

    assert deal_has_changed(r_test, new_deal) is True


def test_deal_collected_from_valid_sites_makes_valid_deals():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    url_bjj = 'http://www.bjjhq.com/'
    deal_bjj = collect_deal(url_bjj, 'bjj')

    assert type(deal_bjj) is DailyDeal
    assert type(deal_bjj.name) is str
    assert type(deal_bjj.price) is int
    assert type(deal_bjj.sport) is str

    url_mma = 'http://www.mmahq.com/'
    deal_mma = collect_deal(url_mma, 'mma')

    assert type(deal_mma) is DailyDeal
    assert type(deal_mma.name) is str
    assert type(deal_mma.price) is int
    assert type(deal_mma.sport) is str


def test_deal_collected_from_invalid_site_returns_none():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    invalid_url = 'http://www.moravian.edu/'
    invalid_deal = collect_deal(invalid_url, 'bjj')

    assert invalid_deal is None


def test_adding_new_deal_replaces_old_deal_position():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal_bjj = DailyDeal('item', int(1), 'bjj')
    update_db(r_test, deal_bjj)

    assert r_test.lindex('product_name', 0).decode().strip() == 'item'
    assert int(r_test.lindex('product_price', 0).decode()) == int(1)
    assert r_test.lindex('product_sport', 0).decode().strip() == 'bjj'

    deal_mma = DailyDeal('other_item', int(5), 'mma')
    update_db(r_test, deal_mma)

    assert r_test.lindex('product_name', 0).decode().strip() == 'other_item'
    assert int(r_test.lindex('product_price', 0).decode()) == int(5)
    assert r_test.lindex('product_sport', 0).decode().strip() == 'mma'


def test_adding_new_deal_moves_old_deal_over_by_one_in_db_list():
    r_test = Redis(host='localhost', port=6379, db=1)
    r_test.flushdb()

    deal_bjj = DailyDeal('item', int(1), 'bjj')
    update_db(r_test, deal_bjj)

    assert r_test.lindex('product_name', 0).decode().strip() == 'item'
    assert int(r_test.lindex('product_price', 0).decode()) == int(1)
    assert r_test.lindex('product_sport', 0).decode().strip() == 'bjj'

    deal_mma = DailyDeal('other_item', int(5), 'mma')
    update_db(r_test, deal_mma)

    assert r_test.lindex('product_name', 1).decode().strip() == 'item'
    assert int(r_test.lindex('product_price', 1).decode()) == int(1)
    assert r_test.lindex('product_sport', 1).decode().strip() == 'bjj'
