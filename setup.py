import setuptools

with open('README.md', 'r', encoding='UTF-8') as f:
      descriptions = f.read()


__version__ = '0.0.0.0'

REPO_NAME = "Email_Spam_Classifier"
AUTHOR_USER_NAME = "HimmatMagar"
SRC_REPO = "emailClassifier"
AUTHOR_EMAIL = "himmatmagar007@gmail.com"

setuptools.setup(
      name="Email Classifier",
      version=__version__,
      author=AUTHOR_USER_NAME,
      author_email=AUTHOR_EMAIL,
      description="End to End Deep Learning implementation for Email Classifier",
      long_description=descriptions,
      long_description_content_type='text/markdown',
      url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
      project_urls={
            "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issue"
      },
      package_dir={"": "src"},
      packages=setuptools.find_packages(where='src')
)
