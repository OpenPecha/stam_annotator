import os
import subprocess

from stam_annotator.definations import ROOT_DIR
from stam_annotator.github_token import GITHUB_TOKEN


class Repo:
    alignment_id: str
    source_org: str
    destination_org: str

    def __init__(self, id_: str, source_org: str):
        self.alignment_id = id_
        self.source_org = source_org
        self.base_path = self.make_local_folder()

    def make_local_folder(self):
        """make local folder to clone the alignment and pecha repo"""
        destination_folder = os.path.join(ROOT_DIR, self.alignment_id)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        return destination_folder

    def get_alignment_repo(self):
        try:
            org, repo_name, token = self.source_org, self.alignment_id, GITHUB_TOKEN
            destination_folder = self.base_path
            repo_url = f"https://{token}@github.com/{org}/{repo_name}.git"
            subprocess.run(["git", "clone", repo_url, destination_folder], check=True)
            print(
                f"Repository {repo_name} cloned successfully into {destination_folder}"
            )

        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name} repository: {e}")


if __name__ == "__main__":
    repo = Repo("AB3CAED2A", "OpenPecha-Data")
    repo.get_alignment_repo()
