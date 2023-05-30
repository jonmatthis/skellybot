import subprocess

from langchain.document_loaders import UnstructuredMarkdownLoader

class DocumentationDownloader:
    """A class that downloads documentation from a URL and parses it into a Python object."""

    def __init__(self, git_url: str, clone_dir: str, docs_folder_name:str='docs'):
        """
        Args:
            git_url (str): The URL of the GitHub repository.
            clone_dir (str): The directory where the cloned repository will be saved.
            features (str): Parser library to be used by BeautifulSoup. Default is 'html.parser'.
        """
        self.git_url = git_url
        self.clone_dir = clone_dir
        self.docs_folder = f'{self.clone_dir}/{docs_folder_name}'

    def clone_repository(self):
        """Clones the GitHub repository."""
        subprocess.run(["git", "clone", self.git_url, self.clone_dir])

    def load(self):
        """Loads the downloaded files using ReadTheDocsLoader.

        Returns:
            The loaded documents.
        """
        loader = UnstructuredMarkdownLoader(self.docs_folder, mode="elements")
        return loader.load()


if __name__ == "__main__":
    downloader = DocumentationDownloader('https://github.com/freemocap/documentation.git', 'freemocap_docs')
    downloader.clone_repository()
    docs = downloader.load()
