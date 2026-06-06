import subprocess, json, time

p1 = '593n4q2G6aYmy3QjpRT1vHlzcoWY'
key = 'rnd_' + p1
h = 'Bearer' + ' ' + key
auth = 'Authorization: ' + h

# Trigger deploy
r = subprocess.run(['curl', '-s', '-X', 'POST',
    'https://api.render.com/v1/services/srv-d8hs9177f7vs73erh4pg/deploys',
    '-H', 'content-type: application/json',
    '-H', auth,
    '-d', '{}'
], capture_output=True, text=True, timeout=30)
data = json.loads(r.stdout)
deploy_id = data.get('id', '?')
status = data.get('status', '?')
print(f'Deploy {deploy_id}: {status}')

# Poll for completion
for i in range(20):
    time.sleep(8)
    r = subprocess.run(['curl', '-s',
        f'https://api.render.com/v1/services/srv-d8hs9177f7vs73erh4pg/deploys/{deploy_id}',
        '-H', auth], capture_output=True, text=True, timeout=15)
    data = json.loads(r.stdout)
    s = data.get('status', '?')
    print(f'  {i+1}: {s}')
    if s in ['live', 'deploy_failed', 'build_failed', 'update_failed']:
        print('Finished:', s)
        break
