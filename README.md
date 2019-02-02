# bchain-metrics
Metrics for block-chain implementation exactly that https://github.com/Xarenn/blockchain

Written in Django and Django Rest Framework

# How it works
Metrics is a server in Python3 which allows communication with the block-chain server and save their state, manage it (of course only in the admin state because block-chain server has own state of chain and it has proof of work implementation)

Admin page have search item where we can find blocks by name of chain etc..

# How to run it?

Use commands:
<code> python3 -m pip install -r requirements.txt </code>
<code> python3 manage.py runserver </code>

or use Docker


![Alt text](img/ss1.png?raw=true "Admin page")
![Alt text](img/ss2.png?raw=true "Admin page")
