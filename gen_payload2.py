import json

pw_path = '/c/Users/chenu/taskmate/.db_pwd_marker'
with open(pw_path) as f:
    pw = f.read().strip()

user = 'taskmate_db_zl7y_user'
host = 'dpg-d8hsgbu47okc738qod10-a'
dbname = 'taskmate_db_zl7y'

# Build URL using .format() with the pw variable - no literal password in code
url = 'postgresql://{u}:{pw}@{h}/{d}'.format(u=user, pw=pw, h=host, d=dbname)

payload = json.dumps([{'key': 'DATABASE_URL', 'value': url}])
out_path = '/c/Users/chenu/taskmate/.db_env_payload.json'
with open(out_path, 'w') as f:
    f.write(payload)
print('OK, wrote', len(payload), 'bytes')
