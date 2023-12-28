from setuptools import setup, find_packages

setup(
    name="errbot-plugin-helloworld",
    version="1.1",
    description="Errbot HelloWorld plugin",
    author="Errbot",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    package_data={
        "helloworld": [
            "*.plug",
        ],
    },
    include_package_data=True,
    entry_points={
        "errbot.plugins": [
            "helloworld = helloworld:HelloWorld",
        ]
    },
)
