import os
import git


class BranchCreator:
	def __init__(self, cwd, on_branch, new_branch):
		if not os.path.exists(cwd):
			self.cwd = os.getcwd()
		else:
			self.cwd = cwd
		self.root = git.Git(self.cwd)
		self.on_branch = on_branch
		self.new_branch = new_branch
		git.Repo(self.cwd).config_writer() \
			.set_value(section="push", option="autoSetupRemote", value=True)
		self.commitLogText = self.root.log(p=True)

	def script_services(self):
		if self.cwd and self.on_branch and self.new_branch:
			if self.checkout():
				print(self.commitLogText)

	def checkout(self):
		remote_branches = []
		# for ref in self.root.branch('-a').split('\n'):
		# 	remote_branches.append(ref)
		if self.on_branch in self.root.branch('-a'):
			print(self.root.branch('-a'))
			self.create_branches()
		else:
			return f"'{self.on_branch}' branch not exist in branch list {remote_branches}"

	def create_branches(self):
		try:
			self.root.fetch("origin")
			self.root.add(".")
			self.root.branch(self.new_branch, self.on_branch)
			self.root.checkout(self.new_branch)
			self.root.push()
		except:
			print(self.commitLogText)


branch_creator = BranchCreator(cwd=r"D:\PROJECTS\LIBRARY_TEST",
							   on_branch="123",
							   new_branch="Test_branch_1_0_0")

branch_creator.script_services()
