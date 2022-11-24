from ..application.cli import TEST_EXPERIENCE_ID_1, TEST_EXPERIENCE_ID_2


async def test_admin_update_experience_capacity(test_client) -> None:
    # Update the experience capacity
    response = await test_client.put(f"/admin/experiences/{TEST_EXPERIENCE_ID_1}", json={'capacity': 25})
    assert response.status_code == 200


async def test_admin_update_experience_capacity_error(test_client) -> None:
    # Update the experience capacity with an invalid value
    response = await test_client.put(f"/admin/experiences/{TEST_EXPERIENCE_ID_2}", json={'capacity': -1})
    assert response.status_code == 400
