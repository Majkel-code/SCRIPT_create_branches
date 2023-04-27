import os
import git


class BranchCreator:
	def __init__(self,cwd,on_branch,new_branch, message):
		if not os.path.exists(cwd):
			self.cwd = os.getcwd()
		else:
			self.cwd = cwd
		self.root = git.Git(self.cwd)
		git.Repo(self.cwd).config_writer()\
			.set_value(section="push",option="autoSetupRemote", value=True)
		self.on_branch = on_branch
		self.new_branch = new_branch
		self.message = message

	def checkout(self):
		remote_branches = []
		for ref in self.root.branch('-a').split('\n'):
			remote_branches.append(ref)
		if self.on_branch in f"remotes/origin/{remote_branches}":
			self.root.fetch("origin")
			self.root.add(".")
			self.root.branch(self.new_branch, self.on_branch)
			self.root.checkout(self.new_branch)
			self.root.push()
		else:
			print("Error")

	def create_branches(self):
		pass



branch_creator = BranchCreator(cwd=r"D:\PROJECTS\LIBRARY_TEST",
			  on_branch="GUI-features",
			  new_branch="Test_script_branch_two",
			  message="Create test branch to check script")

branch_creator.checkout()