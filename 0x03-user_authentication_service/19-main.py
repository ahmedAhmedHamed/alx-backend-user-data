from app import app, AUTH


AUTH.register_user('amongus', 'sus')

app.run(host="0.0.0.0", port="5000")

"""
{
    "email": "amongus",
    "reset_token": "48dd439f-d0be-450c-be4c-02bf25046f11"
}
"""
