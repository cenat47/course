async def test_get_facilities(ac):
    response_post = await ac.post("/facilities/", json={"title": "spa"})

    assert response_post.status_code == 200

    response_get = await ac.get("/facilities/")

    assert response_get.status_code == 200
    facilities = response_get.json()
    assert len(facilities) > 0
