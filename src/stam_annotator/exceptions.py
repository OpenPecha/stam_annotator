class RepoDoesNotExist(Exception):
    """Raised when there is a problem with the repository."""

    def __init__(self, org_name, repo_name):
        self.org_name = org_name
        self.repo_name = repo_name
        self.message = f"Repo {repo_name} does not exist in {org_name}."
        super().__init__(self.message)
