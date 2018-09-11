from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import yaml
import logging

RECEIVER_PORT = 8888
WEBHOOK_CONFIG_FILE = 'config.yaml'

LOG_FORMAT = '[%(asctime)s] %(levelname)-8s: %(message)s'

webhook_config = None


# This class is based on:
# https://gitlab.com/help/user/project/integrations/webhooks
class GitlabReceiver(BaseHTTPRequestHandler):
    def do_POST(self):
        if 'X-Gitlab-Event' not in self.headers:
            self.send_error(404)
            return
        if self.headers['X-Gitlab-Event'] != 'Push Hook':
            self.send_error(404)
            return

        try:
            body = json.load(self.rfile)
            project_name = body['project']['name']
            project_url = body['project']['url']
            ref_branch = body['ref'].split('/')[-1]  # refs/heads/master
            logging.info("Received push event of '{}'({}) in branch '{}'.".format(project_name, project_url, ref_branch))

            found_match = False
            for conf in webhook_config['configs']:
                if project_name == conf['name'] and project_url == conf['url'] and ref_branch == conf['branch']:
                    found_match = True
                    self._run_script(**conf)
            if not found_match:
                logging.info('No config was found.')
            self.send_response_only(200)
        except Exception as e:
            logging.exception(e)
            self.send_error(500)

    def _run_script(self, **kwargs):
        name = kwargs['name']
        script = kwargs['script']
        logging.info("Running '{}' for project {}...".format(script, name))
        try:
            subprocess.run([script])
            logging.info("'{}' script complete.".format(script))
        except Exception as e:
            logging.exception(e)


def main():
    global webhook_config
    try:
        with open(WEBHOOK_CONFIG_FILE, encoding='utf-8') as file:
            webhook_config = yaml.load(file.read())
    except Exception as e:
        print('Failed to open webhook config file.')
        print(e)
        return

    server_address = ('', RECEIVER_PORT)
    server_instance = HTTPServer(server_address, GitlabReceiver)
    print('Starting Gitlab Push Receiver in port {}...'.format(RECEIVER_PORT))
    server_instance.serve_forever()


if __name__ == '__main__':
    # Log to both stdout and file
    logging.basicConfig(filename='receiver.log', filemode='a', level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    main()
