import requests
import time
import matplotlib.pyplot as plt

n_page = 100
if n_page > 100:
    print('오래 걸림')
else:
    t = []
    n = []
    for page in range(1, n_page):
        url = 'https://bitnodes.earn.com/api/v1/snapshots/?limit=100&page=' + str(page)
        resp = requests.get(url=url)
        data = resp.json()
        print('page %d loaded' % page)

        for i in range(len(data['results'])):
            ts = time.gmtime(data['results'][i]['timestamp'])
            t.append(time.strftime('%Y-%m-%d %H:%M:%S', ts))
            n.append(data['results'][i]['total_nodes'])
        
    t = t[::-1]
    n = n[::-1]

    plt.figure(figsize=(8,6))
    plt.plot(n, color='red', linewidth=0.7)
    plt.title('Bitcoin nodes\n' + t[0] + '-' + t[-1])
    plt.grid(color='green', alpha=0.2)
    plt.show()