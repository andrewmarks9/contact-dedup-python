import pandas as pd
from dedup import sanitize, normalize_and_key, deduplicate, find_fuzzy_matches

def test_sanitize():
    assert sanitize(' John  ') == 'john'
    assert sanitize('Smith!@#') == 'smith'
    assert sanitize(' 123 Main St. ') == '123 main st'
    assert sanitize('Apt. 4B') == 'apt 4b'
    assert sanitize('') == ''

def test_normalize_and_key():
    data = {
        'First Name': ['John', 'john', 'Jane'],
        'Last Name': ['Smith', 'Smith', 'Doe'],
        'Address': ['123 Main St', '123 main st', '456 Oak Ave']
    }
    df = pd.DataFrame(data)
    df = normalize_and_key(df, ['First Name', 'Last Name', 'Address'])
    assert 'key' in df.columns
    assert df['key'][0] == df['key'][1]  # John Smith 123 Main St
    assert df['key'][2] != df['key'][0]  # Jane Doe 456 Oak Ave

def test_deduplicate():
    data = {
        'First Name': ['John', 'john', 'Jane'],
        'Last Name': ['Smith', 'Smith', 'Doe'],
        'Address': ['123 Main St', '123 main st', '456 Oak Ave']
    }
    df = pd.DataFrame(data)
    df = normalize_and_key(df, ['First Name', 'Last Name', 'Address'])
    df_dedup = deduplicate(df)
    assert len(df_dedup) == 2  # John Smith 123 Main St and Jane Doe 456 Oak Ave

def test_find_fuzzy_matches():
    keys = ['john|smith|123 main st', 'jon|smith|123 main st', 'jane|doe|456 oak ave']
    matches = find_fuzzy_matches(keys, threshold=90)
    assert any('john|smith|123 main st' in m and 'jon|smith|123 main st' in m for m in [ (a,b) for a,b,_ in matches])

