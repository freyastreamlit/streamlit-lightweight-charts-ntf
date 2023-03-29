import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print('find_packages',setuptools.find_packages())

setuptools.setup(
    name="streamlit-lightweight-charts-ntf",
    version="0.7.18",
    author="Joe Rosa",
    author_email="joe.rosa@itpmngt.co.uk",
    license="UNLICENSED",
    classifiers=[],
    description="Wrapper for TradingView lightweight-charts using ntf fork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/freyastreamlit/streamlit-lightweight-charts-ntf",
    packages=['streamlit_lightweight_charts_ntf'],
    package_dir={'streamlit_lightweight_charts_ntf': 'streamlit_lightweight_charts_ntf'},
    package_data={
        'streamlit_lightweight_charts_ntf.frontend.build': ['*'],
        'streamlit_lightweight_charts_ntf.frontend.build.static.js': ['*']
    },
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.62",
    ],
)
