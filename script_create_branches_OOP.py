import os
import git
import sys


class BranchCreator:
    def __init__(self):
        self.git_root = git.Git()
        self.dir_list = []
        self.on_branch = ""
        self.new_branch = ""
        self.optional = "regular"
        self.repo_dir = ""

    def script_services(self):
        self.take_arguments()
        for repo_dir in self.dir_list:
            self.repo_dir = repo_dir
            cwd = os.path.dirname(os.getcwd())
            print(f"I'm start working on this repo directory: {self.repo_dir}")
            cwd = rf"{cwd}\{self.repo_dir}"
            self.git_root = git.Git(cwd)
            try:
                git.Repo(cwd).config_writer().set_value(
                    section="push", option="autoSetupRemote", value=True
                )
            except:
                print(
                    f"ERROR: Unable to change GIT configuration file in directory: {cwd}, "
                    f"Please check directory and try again."
                )
                continue
            print(f"Take PRIMARY branch: {self.on_branch}")
            print(f"Take NEW branch: {self.new_branch}")
            make_checkout = self.checkout()
            if make_checkout is True:
                self.create_branches()
            else:
                print(make_checkout)
                continue

    def take_arguments(self):
        arguments = sys.argv
        print(arguments)
        flags = {"dir_list": "-dir", "on_branch": "-on", "new_branch": "-new"}
        for key in flags.keys():
            if key == "dir_list":
                self.dir_list = arguments[arguments.index(flags[key]) + 1].split(",")
            elif key == "on_branch":
                self.on_branch = arguments[arguments.index(flags[key]) + 1]
            elif key == "new_branch":
                self.new_branch = arguments[arguments.index(flags[key]) + 1]
            print(self.dir_list, self.on_branch, self.new_branch)
        if "--dynamic" in arguments:
            self.optional = "dynamic"

    def checkout(self):
        remote_branches = []
        for ref in self.git_root.branch("-a").split("\n"):
            if "* " in ref:
                remote_branches.append(ref.replace("* ", ""))
            else:
                remote_branches.append(ref.strip())
        print(remote_branches)
        if (
            self.on_branch not in remote_branches
            and self.on_branch in f"remotes/origin/{remote_branches}"
            and self.new_branch not in f"remotes/origin/{remote_branches}"
        ):
            try:
                self.git_root.checkout(
                    "-b", self.on_branch, f"remotes/origin/{self.on_branch}"
                )
            except:
                remote_branches = []
                for ref in self.git_root.branch("-a").split("\n"):
                    remote_branches.append(ref.strip())
                if self.on_branch in remote_branches:
                    print(remote_branches)
                    return True
        elif (
            self.on_branch in remote_branches
            and self.new_branch not in f"remotes/origin/{remote_branches}"
        ):
            return True
        elif self.on_branch not in f"remotes/origin/{remote_branches}":
            return f"ERROR: '{self.on_branch}' not in {remote_branches}\n on repository directory: {self.repo_dir}"
        elif (
            self.on_branch in f"remotes/origin/{remote_branches}"
            and self.new_branch in f"remotes/origin/{remote_branches}"
        ):
            return f"ERROR: existing {self.new_branch} on {remote_branches}"

    def create_branches(self):
        self.git_root.fetch()
        if self.optional == "regular":
            self.git_root.branch(self.new_branch, self.on_branch)
            self.git_root.checkout(self.new_branch)
            self.git_root.push("origin", self.new_branch)
            print(
                f"'{self.new_branch}' successfully created on '{self.on_branch}' in directory {self.repo_dir}"
            )
        elif self.optional == "dynamic":
            self.git_root.branch(
                f"{self.new_branch}_dynamic", f"{self.on_branch}_dynamic"
            )
            self.git_root.checkout(f"{self.new_branch}_dynamic")
            self.git_root.push(f"-u origin {self.new_branch}_dynamic")
            print(
                f"'{self.new_branch}_dynamic' successfully created on '{self.on_branch}_dynamic' in directory {self.repo_dir}"
            )
        else:
            print(f"script have some problem to create new branch '{self.new_branch}' ")


if __name__ == "__main__":
    branch_creator = BranchCreator()
    branch_creator.script_services()
