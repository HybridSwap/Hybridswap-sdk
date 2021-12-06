import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="hybridswap-py-sdk",
    description="Hybridswap Python SDK",
    author="Hybridswap",
    author_email="hello@hybridswap.org",
    version="0.0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source": "https://github.com/HybridSwap/Hybridswap.live",
    },
    install_requires=["py-algorand-sdk >= 1.6.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    package_data={'hybridswap.v1': ['asc.json']},
    include_package_data=True,
)
