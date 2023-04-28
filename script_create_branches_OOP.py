import os
import time

import git
import sys


class BranchCreator:
	def __init__(self, dir: str, on_branch: str, new_branch: str, optional="regular"):
		cwd = os.path.dirname(os.getcwd())
		print(os.getcwd())
		self.dir = dir
		cwd = fr"{cwd}\{self.dir}"
		self.root = git.Git(cwd)
		print(cwd)
		self.on_branch = on_branch
		self.new_branch = new_branch
		self.optional = optional
		git.Repo(cwd).config_writer() \
			.set_value(section="push", option="autoSetupRemote", value=True)
		self.commitLogText = self.root.log(p=True)

	def script_services(self):
		if self.dir and self.on_branch and self.new_branch:
			self.checkout()

	def checkout(self):
		remote_branches = []
		for ref in self.root.branch('-a').split('\n'):
			remote_branches.append(ref)
		if self.on_branch in f"remotes/origin/{remote_branches}":
			print(remote_branches)
			self.create_branches()
		else:
			print(f"'{self.on_branch}' branch not exist in branch list {remote_branches}")

	def create_branches(self):
		# try:
			self.root.fetch(f"origin {self.on_branch} --prune")
			self.root.add(".")
			if self.optional == "regular":
				self.root.checkout(self.on_branch)
				self.root.branch(self.new_branch, self.on_branch)
				self.root.checkout(self.new_branch)
				self.root.push(f"-u origin {self.new_branch}")
			elif self.optional == "dynamic":
				self.root.branch(f"{self.new_branch}_dynamic",
								 f"{self.on_branch}_dynamic")
				self.root.checkout(f"{self.new_branch}_dynamic")
				self.root.push(f"-u origin {self.new_branch}_dynamic")
		# except Exception:
		# 	print("error")


branch_creator = BranchCreator(
	dir="LIBRARY_TEST",
	on_branch="GUI-features",
	new_branch="Test_branch_dynamic")

branch_creator.script_services()