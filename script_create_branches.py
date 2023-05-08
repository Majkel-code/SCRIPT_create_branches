import os
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
	if on_branch not in remote_branches \
		and on_branch in f"remotes/origin/{remote_branches}" \
		and new_branch not in f"remotes/origin/{remote_branches}":
		try:
			root_git.checkout("-b", on_branch, f"remotes/origin/{on_branch}")
		except:
			remote_branches = []
			for ref in root_git.branch('-a').split('\n'):
				remote_branches.append(ref.strip())
			if on_branch in remote_branches:
				print(remote_branches)
				return True
	elif on_branch in remote_branches and new_branch not in f"remotes/origin/{remote_branches}":
		return True
	elif on_branch not in f"remotes/origin/{remote_branches}":
		return f"ERROR: '{on_branch}' not in {remote_branches}\n on repository directory: {repo_dir}"
	elif on_branch in f"remotes/origin/{remote_branches}" and new_branch in f"remotes/origin/{remote_branches}":
		return f"ERROR: existing {new_branch} on {remote_branches}"


def create_branch(root_git, on_branch, new_branch, optional, repo_dir):
	root_git.fetch()
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
		print(f"I'm start working on this repo directory: {repo_dir}")
		cwd = fr"{cwd}\{repo_dir}"
		root_git = git.Git(cwd)
		git.Repo(cwd).config_writer() \
			.set_value(section="push", option="autoSetupRemote", value=True)
		print(f"Take PRIMARY branch: {on_branch}")
		print(f"Take NEW branch: {new_branch}")
		make_checkout = checkout(root_git, on_branch, new_branch, repo_dir)
		if make_checkout is True:
			create_branch(root_git, on_branch, new_branch, optional, repo_dir)
		else:
			print(make_checkout)
			continue


script_services()
