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

# To do: update the pathes
# Will success:
providor_run_tests_path = "/devOps/CI-server/temp/success"
weight_run_tests_path = "/devOps/CI-server/temp/success/tempTest"
# Will fail:
# providor_run_tests_path = "/devOps/CI-server/temp/fail"
# weight_run_tests_path = "/devOps/CI-server/temp/fail/tempTest"

# global var
version_hash = "production is down."
test_version_hash = "testing is down"


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

    # parsing post request
    cprint('Parsing github webhook POST request...', 'red', 'on_white', attrs=['bold'])
    content = request.json
    pusher = content["pusher"]["name"]
    pusher_email = content["pusher"]["email"]
    head_commit = content["head_commit"]["id"]
    branch_name = os.path.basename(content["ref"])
    cprint("{0} was pushed by {1} on branch {2}\nemail address - {3}\nstart processing...".format(head_commit, pusher,
                                                                                                  branch_name,
                                                                                                  pusher_email),
           attrs=['bold'])

    # trying to free up space
    print("\n\n")
    cprint('Freeing up space...', 'red', 'on_white', attrs=['bold'])
    clean_env()

    # creating a local repository for testing
    print("\n\n")
    cprint('Cloning repository for {0}...'.format(head_commit), 'red', 'on_white', attrs=['bold'])
    repo = repo_dir + head_commit
    create_repo_of_commit(git_url, repo, head_commit)

    # building testing build
    print("\n\n")
    cprint('Building testing environment...', 'red', 'on_white', attrs=['bold'])
    build(repo + weight_path_test, repo + providor_path_test)
    test_version_hash = "Test server: " + branch_name + " - " + head_commit

    # testing build and sending reports
    print("\n\n")
    cprint('Executing tests...', 'red', 'on_white', attrs=['bold'])
    test_passed, results = exec_tests(repo + providor_run_tests_path, repo + weight_run_tests_path)
    if test_passed:
        cprint('All tests passed! sending report...', 'green', attrs=['bold'])
    else:
        cprint('Some tests failed! will not update production. sending report...', 'red', attrs=['bold'])
    sendReport.send_report(test_passed, results, pusher_email, head_commit,
                           branch_name)

    # if the test passed - push to production
    if branch_name == "master" and test_passed:
        print("\n\n")
        cprint('Updating production...', 'red', 'on_white', attrs=['bold'])
        build(repo + weight_path_prod, repo + providor_path_prod)
        shutil.move(repo, master_history_path, copy_function=shutil.copytree)
        version_hash = "Production server: " + branch_name + " - " + head_commit

    print("\n\n")
    cprint('Cleaning up environment...', 'red', 'on_white', attrs=['bold'])
    clean_env()

    print("\n\n")
    print(colored('DONE', 'green', attrs=['reverse', 'blink']))
    return "CI server webhooked".format(content)


def create_repo_of_commit(git_url, repo_dir, commit_hash):
    repo = Repo.clone_from(git_url, repo_dir)
    repo.git.checkout(commit_hash)


def exec_tests(providor_path, weight_path):
    import sys
    sys.path.insert(1, providor_path)
    from testExecProvidor import runTesting
    sys.path.insert(1, weight_path)
    from testExecWeight import execTesting
    providors_state, providors_error_list = runTesting()
    weights_state, weights_error_list = execTesting()
    if providors_state == True and weights_state == True:
        return True, []
    else:
        combined_tests_list = providors_error_list + weights_error_list + ["%d tests failed" % len(providors_error_list + weights_error_list)]
        return False, combined_tests_list


# deleting unused images containers and volumes
def clean_env():
    subprocess.run("docker system prune -af", shell=True)
    subprocess.run("sudo rm -rfd ~/testing/*", shell=True)
    subprocess.run("sudo rm -rfd ~/master_hist/*", shell=True)


def build(weight_path, provider_path):
    cprint('Building weights app...', 'red', 'on_white', attrs=['bold'])
    subprocess.run("docker-compose -f {0} build --no-cache".format(weight_path), shell=True)
    print("\n\n")
    cprint('Composing weights app...', 'red', 'on_white', attrs=['bold'])
    subprocess.run("docker-compose -f {0} up -d".format(weight_path), shell=True)
    print("\n\n")
    cprint('building providers app...', 'red', 'on_white', attrs=['bold'])
    subprocess.run("docker-compose -f {0} build --no-cache".format(provider_path), shell=True)
    print("\n\n")
    cprint('Composing providers app...', 'red', 'on_white', attrs=['bold'])
    subprocess.run("docker-compose -f {0} up -d".format(provider_path), shell=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
