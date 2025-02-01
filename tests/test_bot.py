def test_semantic_search():
    query = "My table is missing"
    expected_error = "ORA-00942"
    assert search_error(query) == expected_error

def test_feedback_storage():
    log_feedback("ORA-00942", True)
    assert get_upvotes("ORA-00942") > 0
