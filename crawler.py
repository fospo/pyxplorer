import os
import logging
from github import Github
import concurrent.futures


def dry_run(inputOrg: str) -> bool:
    """Working just on GitHub for the moment"""
    MAX_WORKERS = 10
    GH_TOKEN = os.getenv("GH_TOKEN")
    g = Github(GH_TOKEN)

    # get paginated result of repos
    orgRepos = g.get_organization(inputOrg).get_repos()

    # threadpool setup and launch
    try:
        threadPool = concurrent.futures.ThreadPoolExecutor(MAX_WORKERS)
        threadPool.map(exploreLicenses, orgRepos)
    except Exception:
        logging.error("Error in thread pool execution.")
        return False
    finally:
        # Shutdown waits for all threads to finish by default
        threadPool.shutdown()

    return True


def exploreLicenses(repository: str):
    """Exploring the repository (input) and printing the license.name"""
    try:
        license = repository.get_license()
        print(repository.name + "," + license.license.name)
    except Exception:
        print(repository.name + "," + "Empty")