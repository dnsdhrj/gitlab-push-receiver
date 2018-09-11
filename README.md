# GitLab Push Receiver
Detect GitLab push events using [webhook](https://gitlab.com/help/user/project/integrations/webhooks), and run custom scripts. (ex. auto-deploy)

Can be used as a webhook router, with single entry point.

Use with simple project which does not have CI.

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
