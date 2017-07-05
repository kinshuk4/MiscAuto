import subprocess
import time
import sys
import re


# https://gist.github.com/blackfalcon/8428401
# https://gist.github.com/CyberShadow/1885859
def switch_to_master():
    commands = ["git checkout master", "git pull origin master"]
    for command in commands:
        bash_command(command)


def get_new_branch(branchName):
    switch_to_master()
    checkout_cmd = "git checkout -b " + branchName
    bash_command(checkout_cmd)


def switch_to_branch(branchName):
    checkout_cmd = "git checkout " + branchName
    bash_command(checkout_cmd)


def commit_n_push_new_branch(issueNum, issueString, branchName):
    commitMsg = '"' + 'ISSUE-' + issueNum + ' ' + issueString + '"'
    commands = ["git add --all", 'git commit -m  ' + commitMsg,
                "git push origin " + branchName]
    bash_commands(commands)


def generate_pr(issueNum, branchName):
    # commands = ["git checkout " + branchName, "git pull origin " + branchName, "git pull origin master",
    #             "git checkout master", "git pull origin master"]
    # for command in commands:
    #     print(bash_command(command))
    print("here")
    url = bash_command(
        "git config --get remote.origin.url  | sed -e 's#^[^:/]\+:\(//[^/]\+/\)\?#https://github.com/#' -e 's#\.git$##' -e 's#/$##'")
    print(str(url))
    switch_to_branch(branchName)
    output = bash_command("git pull-request master")
    return output


def delete_branch(branchName):
    bash_command("git branch -d " + branchName)


def git_sync(branchName):
    commands = ["git checkout " + branchName, "git pull", "git push origin " + branchName]
    bash_commands(commands)


def bash_commands(commands):
    for command in commands:
        bash_command(command)


def bash_command(command):
    # remove all multiple whitespace to one
    shell = False
    command = re.sub(' +', ' ', command)
    if ('|' in command):
        shell = True
    if '"' in command or "'" in command:
        if '"' in command:
            split_command_without_quotes = command.split('"')
        elif "'" in command:
            split_command_without_quotes = command.split("'")

        split_command = split_command_without_quotes[0].rstrip().split(" ")
        split_command.append(split_command_without_quotes[1])
    else:
        split_command = command.split(" ")

    if shell:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = process.communicate()[0]
    else:
        print(split_command)
        process = subprocess.Popen(split_command)
        output = process.communicate()
    return output


def bash_command_simple(command):
    process = subprocess.Popen(command)
    output = process.communicate()
    return output


# def input(message):
#     print(message)
#     entered_data = sys.stdin.read()
#     return str(entered_data)


def prompt_yes(message):
    entered_data = input(message)
    if "y" is entered_data:
        return True
    else:
        return prompt_yes(message)


def workflow(issueNum, issueString):
    issueStringBranch = issueString.lower().replace(" ", "-")
    branchName = "ISSUE-" + str(issueNum) + "-" + str(issueStringBranch)

    print("Checking out the new branch: ", branchName)
    # get_new_branch(branchName)
    switch_to_branch(branchName)
    git_sync(branchName)
    print("Switched to new branch: {}. Please start coding and let me know when I can commit", branchName)
    # yes = prompt_yes("Should I add and commit? [y/n]")
    #
    # if yes:
    #     commit_n_push_new_branch(issueNum, issueString, branchName)

    option = input("Pull request: 1 , commit: 2, delete: 3 , done: 4?")
    while option is not "3" or "4":
        if option is "1":
            output = generate_pr(issueNum, branchName)
            print(output)
        elif option is "2":
            output = input("Please tell message for commit: ")
            commit_n_push_new_branch(issueNum, output, branchName)
        elif option is "3":
            print("Deleting the branch.")
            delete_branch
        elif option is "4":
            print("we are done now")


def main():
    issueNum = input("Enter the issue number you are working on:").rstrip()
    issueString = input("Enter the issue string:").rstrip()
    workflow(issueNum, issueString)


def test():
    issueNum = "ddd"
    issueString = "adafad adafda"
    workflow(issueNum, issueString)


if __name__ == '__main__':
    # main()
    test()
