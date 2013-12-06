from mock import Mock, patch

from helga.plugins import haiku


@patch('helga.plugins.haiku.get_random_line')
def test_fix_repitition_replaces(get_random_line):
    poem = ['foo', 'bar', 'foo']
    get_random_line.return_value = 'baz'
    poem = haiku.fix_repitition(poem)

    assert poem == ['foo', 'bar', 'baz']


@patch('helga.plugins.haiku.get_random_line')
def test_fix_repititions_gives_up_after_retry(get_random_line):
    poem = ['foo', 'bar', 'foo']
    get_random_line.return_value = 'foo'
    poem = haiku.fix_repitition(poem)

    assert poem == ['foo', 'bar', 'foo']
    assert haiku.get_random_line.call_count == 2


@patch('helga.plugins.haiku.get_random_line')
def test_fix_repitition_does_not_replace(get_random_line):
    poem = ['foo', 'bar', 'baz']
    poem = haiku.fix_repitition(poem)

    assert poem == ['foo', 'bar', 'baz']
    assert not haiku.get_random_line.called


@patch('helga.plugins.haiku.db')
def test_add(db):
    haiku.add(5, 'foobar')
    assert db.haiku.insert.called


@patch('helga.plugins.haiku.db')
def test_remove(db):
    haiku.remove(5, 'foobar')
    assert db.haiku.remove.called


@patch('helga.plugins.haiku.db')
def test_get_random_line(db):
    result = Mock()
    result.sort = result
    result.count.return_value = 1
    result.limit.return_value = result
    result.skip.return_value = result
    result.next.return_value = {'message': 'fives1'}

    fake_find = Mock(return_value=result)

    db.haiku.find = fake_find
    line = haiku.get_random_line(5)
    assert line == 'fives1'


@patch('helga.plugins.haiku.db')
def test_get_random_line_returns_none(db):
    db.haiku.find.return_value = db
    db.count.return_value = 0
    assert haiku.get_random_line(5) is None


@patch('helga.plugins.haiku.add')
@patch('helga.plugins.haiku.make_poem')
def test_use_fives(make_poem, add):
    make_poem.return_value = ['one', 'two', 'three']
    poem = haiku.use(5, 'foo')
    assert 'foo' in (poem[0], poem[2])


@patch('helga.plugins.haiku.add')
@patch('helga.plugins.haiku.make_poem')
def test_use_fives_does_not_duplicate(make_poem, add):
    make_poem.return_value = ['foo', 'two', 'three']
    poem = haiku.use(5, 'foo')
    assert poem[0] == 'foo'
    assert poem[2] != 'foo'


@patch('helga.plugins.haiku.add')
@patch('helga.plugins.haiku.make_poem')
def test_use_sevens(make_poem, add):
    make_poem.return_value = ['one', 'two', 'three']
    poem = haiku.use(7, 'foo')
    assert poem[1] == 'foo'