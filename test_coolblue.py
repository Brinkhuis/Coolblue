import data_collection

def test_npages():
    url = 'https://www.coolblue.nl/producttype:mobiele-telefoons'
    n = data_collection.npages(url)
    assert type(n) == int, "Should be True"

def test_get_productinfo():
    url = 'https://www.coolblue.nl/producttype:mobiele-telefoons'
    productinfo = data_collection.get_productinfo(url + '?pagina={1}')
    assert productinfo.shape[0] > 0, "Should be greater than 0"

