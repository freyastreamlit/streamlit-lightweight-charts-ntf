import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-lightweight-charts-ntf",
    version="0.7.18",
    author="Joe Rosa",
    author_email="joe.rosa@itpmngt.co.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description="Wrapper for TradingView lightweight-charts using ntf fork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/freyastreamlit/streamlit-lightweight-charts-ntf",
    packages=['streamlit_lightweight_charts_ntf'],
    package_data={
        'streamlit_lightweight_charts_ntf': ['frontend/build/*','frontend/build/static/js/*'],
    },
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.62",
    ],
)
