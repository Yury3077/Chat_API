import requests as re
import json

url = 'http://127.0.0.1:8000'

# data = {"name_chat": 'Cats', "descr": 'British'}  # Запрос для создания чата
# data2 = {"name_chat": 'Trololo1'}  # Запрос на удалени из чата
# data3 = {"name_chat": 'Trololo123', "nick_name": 'BUN'}  # Запрос для добавления пользователя в чат
data4 = {"name_chat": 'Trololo123', "nick_name": 'BUN'}  # Запрос для удаления  пользователя из чата

headers = {'content-type': 'application/json'}
# r = re.post(url + '/api/banton/new_chat', data=json.dumps(data), headers=headers)
# r = re.post(url + '/api/banton/remove_chat', data=json.dumps(data2), headers=headers)
# r = re.post(url + '/api/banton/new_user', data=json.dumps(data3), headers=headers)
r = re.post(url + '/api/banton/remove_user', data=json.dumps(data4), headers=headers)
print(r)
