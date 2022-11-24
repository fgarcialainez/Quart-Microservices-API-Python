from application.cli import TEST_EXPERIENCE_ID_1


async def test_customer_retrieve_experiences(test_client) -> None:
    # Get the test client
    response = await test_client.get("/customer/experiences")
    assert response.status_code == 200
    data = await response.get_json()
    assert 'experiences' in data
    assert len(data['experiences']) > 0


async def test_customer_book_experience(test_client) -> None:
    # Get the test client
    json_body = {'experience_id': TEST_EXPERIENCE_ID_1, 'quantity': 1}
    response = await test_client.post("/customer/book", json=json_body)
    assert response.status_code == 200


async def test_customer_book_experience_error(test_client) -> None:
    # Get the test client
    json_body = {'experience_id': TEST_EXPERIENCE_ID_1, 'quantity': -10}
    response = await test_client.post("/customer/book", json=json_body)
    assert response.status_code == 400
