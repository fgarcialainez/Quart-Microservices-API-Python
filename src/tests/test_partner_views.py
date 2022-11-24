import uuid

from ..application.cli import TEST_EXPERIENCE_ID_1, TEST_PARTNER_ID_WITH_EXPERIENCES, \
    TEST_PARTNER_ID_WITHOUT_EXPERIENCES


async def test_partner_fetch_experiences(test_client) -> None:
    # Get all the experiences for a partner
    response = await test_client.get(f"/partner/experiences?partner_id={TEST_PARTNER_ID_WITH_EXPERIENCES}")
    assert response.status_code == 200
    data = await response.get_json()
    assert 'experiences' in data
    assert len(data['experiences']) > 0


async def test_partner_fetch_experiences_no_data(test_client) -> None:
    # Get all the experiences for a partner
    response = await test_client.get(f"/partner/experiences?partner_id={TEST_PARTNER_ID_WITHOUT_EXPERIENCES}")
    assert response.status_code == 200
    data = await response.get_json()
    assert 'experiences' in data
    assert len(data['experiences']) == 0


async def test_partner_fetch_experience(test_client) -> None:
    # Get an experience for a partner
    response = await test_client.get(f"/partner/experiences/{TEST_EXPERIENCE_ID_1}")
    assert response.status_code == 200


async def test_partner_fetch_experience_no_data(test_client) -> None:
    # Get an experience for a partner no data
    response = await test_client.get(f"/partner/experiences/{str(uuid.uuid4())}")
    assert response.status_code == 400


async def test_partner_update_experience_availability(test_client) -> None:
    # Update the experience availability
    json_body = {'available': True}
    response = await test_client.put(f"/partner/experiences/{TEST_EXPERIENCE_ID_1}", json=json_body)
    assert response.status_code == 200


async def test_partner_update_experience_availability_error(test_client) -> None:
    # Update the experience without availability param
    response = await test_client.put(f"/partner/experiences/{TEST_EXPERIENCE_ID_1}")
    assert response.status_code == 400
