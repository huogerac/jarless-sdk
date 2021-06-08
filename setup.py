from setuptools import setup

setup(
    name="jarlesssdk",
    version="0.0.1",
    py_modules=[
        "jarless_sdk",
    ],
    install_requires=["Click", "docker==4.4.4", "PyYAML==5.4.1"],
    entry_points="""
        [console_scripts]
        jarless=jarless_sdk.sdk:cli
    """,
)
