import os
import subprocess
import yaml
from flask import Flask, request
from git import Repo
import shutil
import sendReport
from termcolor import colored, cprint

# Standard Flask app
app = Flask(__name__)

# Configuration
git_url = "git@github.com:BlueTeam2019/Blue.git"
repo_dir = "/home/ubuntu/testing/"
weight_path_test = "/weight/docker-compose_test.yml"
providor_path_test = "/awesome_provider/docker-compose.yml"
weight_path_prod = "/weight/docker-compose.yml"
providor_path_prod = "/awesome_provider/docker-compose.yml"
master_history_path = "/home/ubuntu/master_hist"

# global var
version_hash = "production is down."
test_version_hash = "testing is down"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Standard Flask endpoint
@app.route("/", )
def hello_world():
    global version_hash
    global test_version_hash
    return version_hash + "<br>" + test_version_hash


# webhook to github
@app.route('/webhook', methods=['POST'])
def webhook():
    print(colored('Incoming push!!!', 'red', attrs=['reverse', 'blink']))
    global version_hash
    global test_version_hash
    # trying to free up space
    cprint('Freeing up space...', 'red', 'on_white', attrs=['bold'])
    clean_env()

    # parsing post request
    content = request.json
    pusher = content["pusher"]["name"]
    pusher_email = content["pusher"]["email"]
    head_commit = content["head_commit"]["id"]
    branch_name = os.path.basename(content["ref"])

    # creating a local repository for testing
    repo = repo_dir + head_commit
    create_repo_of_commit(git_url, repo, head_commit)

    # building testing build
    build(repo + weight_path_test, repo + providor_path_test)
    test_version_hash = "Test server: " + branch_name + " - " + head_commit

    # testing build and sending reports
    test_passed, results = exec_tests()
    sendReport.send_report(test_passed, results, pusher_email)

    # if the test passed - push to production
    if branch_name == "master" and test_passed:
        build(repo + weight_path_prod, repo + providor_path_prod)
        shutil.move(repo, master_history_path, copy_function=shutil.copytree)
        version_hash = "Production server: " + branch_name + " - " + head_commit

    clean_env()
    return "CI server webhooked".format(content)


def create_repo_of_commit(git_url, repo_dir, commit_hash):
    repo = Repo.clone_from(git_url, repo_dir)
    repo.git.checkout(commit_hash)


# implement
def exec_tests():
    return True, ["Test 1: pass", "Test 2: pass"]


# deleting unused images containers and volumes
def clean_env():
    subprocess.run("docker system prune -af", shell=True)
    subprocess.run("sudo rm -rfd ~/testing/*", shell=True)
    subprocess.run("sudo rm -rfd ~/master_hist/*", shell=True)


def build(weight_path, provider_path):
    subprocess.run("docker-compose -f {0} build --no-cache".format(weight_path), shell=True)
    subprocess.run("docker-compose -f {0} up -d".format(weight_path), shell=True)
    subprocess.run("docker-compose -f {0} build --no-cache".format(provider_path), shell=True)
    subprocess.run("docker-compose -f {0} up -d".format(provider_path), shell=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
