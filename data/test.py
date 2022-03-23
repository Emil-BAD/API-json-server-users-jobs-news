from requests import get, post, delete, put

print(get('http://localhost:5000/api/users').json())
# print(post('http://localhost:5000/api/jobs', json={  # коректный запрос
#     'id': 11,
#     'job': "Делать пельмешки",
#     'work_size': 100,
#     'collaborators': 3,
#     'is_finished': False,
#     'team_leader': 1}).json())
print(post('http://localhost:5000/api/users', json={  # коректный запрос
    'id': 4,
    'name': "Эмиль",
    'about': "О себе",
    'email': 'hat-pay@mail.ru',
    'hashed_password': '12341234'}).json())
print(get('http://localhost:5000/api/users').json())

