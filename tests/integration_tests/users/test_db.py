async def test_register_user(db):
    user_data = await db.users.get_all()
    assert user_data
