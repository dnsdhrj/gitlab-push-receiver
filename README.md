# GitLab Push Receiver
Detect GitLab push events using [webhook](https://gitlab.com/help/user/project/integrations/webhooks), and run custom scripts. (ex. auto-deploy)

Can be used as a webhook router, with single entry point.

It is basically minimal CI you can think of.

# Workflow Example
1. Push to GitLab branch
1. Server receives event and automatically runs `deploy.sh`
1. Project is deployed!

# Setup
```bash
pip install -r requirements.txt
vim config.yaml # Set config
```
Then add some hooks in: Project > Settings > Integrations > Integrations.

# Run Server
```bash
python receiver.py
```
