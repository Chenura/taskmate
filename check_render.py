import subprocess, json

t = "593n4q2G6aYmy3QjpRT1vHlzcoWY"
k = "rnd_593n4q2G6aYmy3QjpRT1vHlzcoWY"
a = "Authorization: Bearer "
h = a + k

r = subprocess.run(["curl", "-s", "https://api.render.com/v1/services/srv-d8hs9177f7vs73erh4pg", "-H", h], capture_output=True, text=True, timeout=15)
print(r.stdout[:300])
