from setuptools import setup

setup(
    name="jarlesssdk",
    version="0.0.3",
    py_modules=[
        "jarless_sdk",
    ],
    install_requires=["Click", "docker>=4.3.0", "PyYAML>=5.0.0"],
    entry_points="""
        [console_scripts]
        jarless=jarless_sdk.sdk:cli
    """,
)
