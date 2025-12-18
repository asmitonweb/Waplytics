from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __init__.py
from waplytics import __version__ as version

setup(
	name="waplytics",
	version=version,
	description="The Ultimate Open-Source WhatsApp Analytics Engine",
	author="Asmit",
	author_email="hello@asmitonweb.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
