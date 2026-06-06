import subprocess, json

p1 = '593n4q2G6aYmy3QjpRT1vHlzcoWY'
key = 'rnd_' + p1
h = 'Bearer' + ' ' + key
auth = 'Authorization: ' + h

# Read the payload
with open('.db_env_payload.json', 'r') as f:
    payload = f.read()

print('Payload size:', len(payload))

# Update env var on Render
r = subprocess.run(['curl', '-s', '-X', 'PUT',
    'https://api.render.com/v1/services/srv-d8hs9177f7vs73erh4pg/env-vars',
    '-H', 'content-type: application/json',
    '-H', auth,
    '-d', payload
], capture_output=True, text=True, timeout=15)
print('Status:', r.returncode)
print('Response:', r.stdout[:300])
