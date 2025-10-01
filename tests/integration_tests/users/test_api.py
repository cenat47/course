import pytest
@pytest.mark.parametrize("email, password, status_code", [
    ("wer@qwe.qw","12345", 200),
    ("wer@qwe.","12345", 422),
    ("wer@qwe.qw","12345", 409),
    ])
async def test_flou_auth(email, password, status_code, ac, db):
    registrate_data= {"email": email, "password": password}

    response_reg = await ac.post(
        url="/auth/register",
        json=
                registrate_data
        
    )
    response_reg.status_code == status_code
    if status_code != 200:
        return None
    query = db.users.get_all(email = registrate_data["email"])
    assert query

    response_log = await ac.post(
        url="/auth/login",
        json=registrate_data
    )
    assert response_log.cookies

    response_me = await ac.post(
        url="auth/me"
    )
    res = response_me.json()
    assert res

    response_logout = await ac.post(
        url="auth/logout"
    )
    assert not response_logout.cookies