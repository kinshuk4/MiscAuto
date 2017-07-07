import subprocess
import time
import sys
import re
import json


# https://gist.github.com/blackfalcon/8428401
# https://gist.github.com/CyberShadow/1885859
class IssueState:
    NoBranch = 1
    BranchCreated = 2
    FirstCommitDone = 3
    InFlow = 4
    Delete = 5


class GithubHelper:
    @staticmethod
    def sync_master():
        commands = ["git checkout master", "git pull origin master"]
        for command in commands:
            bash_command(command)

    @staticmethod
    def create_new_branch(branchName):
        checkout_cmd = "git checkout -b " + branchName
        bash_command(checkout_cmd)

    @staticmethod
    def switch_to_branch(branchName):
        checkout_cmd = "git checkout " + branchName
        bash_command(checkout_cmd)

    @staticmethod
    def push_branch(branchName):
        command = ["git push origin " + branchName]
        bash_commands(command)

    @staticmethod
    def commit_change(commit_msg):
        commands = ["git add --all", 'git commit -m  ' + commit_msg]
        bash_commands(commands)

    @staticmethod
    def generate_pr(branchName):
        url = bash_command(
            "git config --get remote.origin.url  | sed -e 's#^[^:/]\+:\(//[^/]\+/\)\?#https://github.com/#' -e 's#\.git$##' -e 's#/$##'")
        print(str(url))
        GithubHelper.switch_to_branch(branchName)
        output = bash_command("git pull-request master")
        return output

    @staticmethod
    def delete_branch(branchName):
        bash_command("git branch -d " + branchName)

    @staticmethod
    def git_sync(branchName):
        commands = ["git checkout " + branchName, "git pull", "git push origin " + branchName]
        bash_commands(commands)


class GithubProcessor:
    def __init__(self, issueNum, issueString):
        self.issueNum = issueNum
        self.issueString = issueString
        issueStringBranch = issueString.lower().replace(" ", "-")
        self.commitIssue = "ISSUE-" + str(issueNum) + "-"
        self.branchName = self.commitIssue + str(issueStringBranch)
        self.state = IssueState.NoBranch

    def create_branch(self):
        print("Creating the new branch: ", self.branchName)
        GithubHelper.sync_master()
        if self.state == IssueState.NoBranch:
            GithubHelper.create_new_branch(self.branchName)
            self.state = IssueState.BranchCreated
        else:
            self.switch_branch()

    def commit_n_push(self, message=None):
        if self.state == IssueState.BranchCreated:
            yes = prompt_yes("Should I add and commit and push? [y/n]")
            commit_msg = '"' + 'ISSUE-' + self.issueNum + ' ' + self.issueString + '"'
            GithubHelper.commit_change(commit_msg)
            self.state = IssueState.FirstCommitDone
            GithubHelper.push_branch(self.branchName)
        elif message is None:
            raise Exception(self.issueNum + "No message to commit to")

    def switch_branch(self):
        GithubHelper.switch_to_branch(self.branchName)

    def generate_pr(self):
        return GithubHelper.generate_pr(self.branchName)


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
    p = GithubProcessor(issueNum, issueString)
    p.create_branch()
    p.commit_n_push()

    option = input("Pull request: 1 , commit: 2, delete: 3 , done: 4? ")
    while option is not "3" or "4":
        if option is "1":
            output = p.generate_pr()
            print(output)
        elif option is "2":
            output = input("Please tell message for commit: ")
            p.commit_n_push(output)
        elif option is "3":
            print("Deleting the branch.")
            # delete_branch
        elif option is "4":
            print("we are done now")


def main():
    issueNum = input("Enter the issue number you are working on:").rstrip()
    issueString = input("Enter the issue string:").rstrip()
    workflow(issueNum, issueString)


def test():
    issueNum = "60"
    issueString = "Deploy fallback Solrs to eu-west-1"
    workflow(issueNum, issueString)


if __name__ == '__main__':
    main()
    # test()
