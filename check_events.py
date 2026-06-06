import subprocess, json

p1 = '593n4q2G6aYmy3QjpRT1vHlzcoWY'
key = 'rnd_' + p1
h = 'Bearer' + ' ' + key
auth = 'Authorization: ' + h

# Get recent events
r = subprocess.run(['curl', '-s',
    'https://api.render.com/v1/services/srv-d8hs9177f7vs73erh4pg/events?limit=10',
    '-H', auth], capture_output=True, text=True, timeout=15)
data = json.loads(r.stdout)
for item in data:
    ev = item.get('event', {})
    ev_type = ev.get('type', '?')
    details = ev.get('details', {})
    if ev_type == 'deploy_ended':
        status = details.get('deployStatus', details.get('status', '?'))
        reason = details.get('reason', {})
        print(f'Deploy ended: status={status}, reason={json.dumps(reason)}')
    elif ev_type == 'deploy_failed':
        print(f'Deploy failed: {json.dumps(details)[:300]}')
    else:
        d = json.dumps(details)[:200]
        print(f'{ev_type}: {d}')
