import os
import time

import git
import sys

def take_arguments():
	dir_list = sys.argv[1].split(",")
	on_branch = sys.argv[2]
	new_branch = sys.argv[3]
	try:
		optional = sys.argv[4]
	except:
		optional = "regular"
	return dir_list, on_branch, new_branch, optional


def checkout(root_git, on_branch: str, new_branch: str, repo_dir):
	remote_branches = []
	for ref in root_git.branch('-a').split('\n'):
		remote_branches.append(ref.strip())
		print(remote_branches)
	if on_branch not in remote_branches and on_branch in f"remotes/origin/{remote_branches}" and new_branch not in f"remotes/origin/{remote_branches}":
		root_git.branch("-f",on_branch, f"origin/{on_branch}")
		return True
	elif on_branch in remote_branches and new_branch not in f"remotes/origin/{remote_branches}":
		return True
	elif on_branch not in f"remotes/origin/{remote_branches}":
		return f"'{on_branch}' not in {remote_branches}\n on repository directory: {repo_dir}"
	elif on_branch in f"remotes/origin/{remote_branches}" and new_branch in f"remotes/origin/{remote_branches}":
		return f"existing {new_branch} on {remote_branches}"


def create_branch(root_git, on_branch, new_branch, optional,repo_dir):
	root_git.fetch(f"origin")
	if optional == "regular":
		root_git.branch(new_branch, on_branch)
		root_git.checkout(new_branch)
		root_git.push("origin", new_branch)
		print(f"'{new_branch}' successfully created on '{on_branch}' in directory {repo_dir}")
	elif optional == "dynamic":
		root_git.branch(f"{new_branch}_dynamic",
						f"{on_branch}_dynamic")
		root_git.checkout(f"{new_branch}_dynamic")
		root_git.push(f"-u origin {new_branch}_dynamic")
		print(f"'{new_branch}_dynamic' successfully created on '{on_branch}_dynamic' in directory {repo_dir}")
	else:
		print(f"script have some problem to create new branch '{new_branch}' ")

def script_services():
	args = take_arguments()
	dir_list = args[0]
	on_branch = args[1]
	new_branch = args[2]
	optional = args[3]
	for repo_dir in dir_list:
		cwd = os.path.dirname(os.getcwd())
		print(os.getcwd())
		cwd = fr"{cwd}\{repo_dir}"
		root_git = git.Git(cwd)
		git.Repo(cwd).config_writer() \
			.set_value(section="push", option="autoSetupRemote", value=True)
		print(on_branch)
		print(new_branch)
		make_checkout = checkout(root_git, on_branch, new_branch, repo_dir)
		if make_checkout is True:
			create_branch(root_git, on_branch, new_branch, optional, repo_dir)
		elif make_checkout is False:
			print(make_checkout)
			continue


script_services()
