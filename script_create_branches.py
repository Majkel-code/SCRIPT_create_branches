import os
import git
import sys
from pathlib import Path


def help_desc():
	"""Create multiple branches

	Create new branch and push to origin

	ARGUMENTS
	-----------
	-dir: str/list
		directory name where repository is stored
		if multiple arguments then every must be after comma ","
		-dir arg1,arg2,arg3 etc.
	-on: str
		primary branch from where we make copy of files
		-on on_branch
	-new: str
		name of new branch to create
		-new new_branch
	--dynamic: str
		use this flag on the end of script invoke if branches are
		on "dynamic" repository

	EXAMPLE
	-----------
	python ./script/path -dir arg1,arg2 -on on_branch -new new_branch
	"""


def take_arguments():
	"""
	Take arguments from console save them to specific variables
	and return it to script_services function
	:return: arguments
	"""
	arguments = sys.argv
	if "--help" in arguments:
		print(help_desc.__doc__)
		exit()
	flags = {"dir_list": "-dir", "on_branch": "-on", "new_branch": "-new"}
	for key in flags:
		try:
			if key == "dir_list":
				directory_list = arguments[arguments.index(flags[key]) + 1].split(",")
			elif key == "on_branch":
				on_branch = arguments[arguments.index(flags[key]) + 1]
			elif key == "new_branch":
				new_branch = arguments[arguments.index(flags[key]) + 1]
		except:
			print(help_desc.__doc__)
			exit()

	if "--dynamic" in arguments:
		optional = "dynamic"
	else:
		optional = "regular"

	return directory_list, on_branch, new_branch, optional


def checkout(root_git, on_branch: str, new_branch: str, repo_dir):
	"""
	Function is checking local and remote branches and if everything is
	correct then return True or print error with message \n
	:param root_git: git object
	:param on_branch: base branch name
	:param new_branch: new branch name
	:param repo_dir: directory of repository
	:return: specific message
	"""
	remotes_origin = "remotes/origin/"
	remote_branches = []
	for ref in root_git.branch("-a").split("\n"):
		if "* " in ref:
			remote_branches.append(ref.replace("* ", ""))
		else:
			remote_branches.append(ref.strip())
	print(remote_branches)
	if (
			on_branch not in remote_branches
			and on_branch in f"{remotes_origin}{remote_branches}"
			and new_branch not in f"{remotes_origin}{remote_branches}"
	):
		try:
			root_git.checkout("-b", on_branch, f"{remotes_origin}{on_branch}")
		except:
			remote_branches = []
			for ref in root_git.branch("-a").split("\n"):
				remote_branches.append(ref.strip())
			if on_branch in remote_branches:
				print(remote_branches)
				return True
	elif (
			on_branch in remote_branches
			and new_branch not in f"{remotes_origin}{remote_branches}"
	):
		return True
	elif on_branch not in f"{remotes_origin}{remote_branches}":
		return f"ERROR: '{on_branch}' not in {remote_branches} on repository directory: {repo_dir}"
	elif (
			on_branch in f"{remotes_origin}{remote_branches}"
			and new_branch in f"{remotes_origin}{remote_branches}"
	):
		return f"ERROR: existing {new_branch} on {remote_branches}"


def create_branch(root_git, on_branch: str, new_branch: str, optional: str, repo_dir):
	"""
	Function creating branch locally then push it to remote repository \n
	:param root_git: git object
	:param on_branch: base branch name
	:param new_branch: new branch name
	:param optional: optional argument for specific repositories
	:param repo_dir: directory of repository
	:return: specific message
	"""
	root_git.fetch()
	if optional == "regular":
		root_git.branch(new_branch, on_branch)
		root_git.checkout(new_branch)
		root_git.push("origin", new_branch)
		print(
			f"'{new_branch}' successfully created on '{on_branch}' in directory {repo_dir}"
		)
	elif optional == "dynamic":
		root_git.branch(f"{new_branch}_dynamic", f"{on_branch}_dynamic")
		root_git.checkout(f"{new_branch}_dynamic")
		root_git.push(f"-u origin {new_branch}_dynamic")
		print(
			f"'{new_branch}_dynamic' successfully created on '{on_branch}_dynamic' in directory {repo_dir}"
		)
	else:
		print(f"script have some problem to create new branch '{new_branch}' ")


def script_services():
	"""
	Main body of script \n
	"""
	args = take_arguments()
	dir_list = args[0]
	on_branch = args[1]
	new_branch = args[2]
	optional = args[3]
	cwd = Path.cwd().parent
	for repo_dir in dir_list:
		print(f"I'm start working on this repo directory: {repo_dir}")
		cwd = rf"{cwd}\{repo_dir}"
		root_git = git.Git(cwd)
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
		print(f"Take PRIMARY branch: {on_branch}")
		print(f"Take NEW branch: {new_branch}")
		make_checkout = checkout(root_git, on_branch, new_branch, repo_dir)
		if make_checkout is True:
			create_branch(root_git, on_branch, new_branch, optional, repo_dir)
		else:
			print(make_checkout)



script_services()
