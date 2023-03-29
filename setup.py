import os
import setuptools

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('streamlit_lightweight_charts_ntf/frontend/build')

print('extra_files',extra_files)

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    include_package_data = True,
    packages=['streamlit_lightweight_charts_ntf','streamlit_lightweight_charts_ntf/frontend'],
    # package_dir={'streamlit_lightweight_charts_ntf': 'streamlit_lightweight_charts_ntf'},
    package_data={
        'streamlit_lightweight_charts_ntf': ['frontend/package.json'],
        'streamlit_lightweight_charts_ntf/frontend': [
            'build/index.html',
            # 'frontend/build/static/js/*',
            # 'frontend/build/index.html',
        ],
    },

    # package_data={
    #     'streamlit_lightweight_charts_ntf' : ['frontend/build/*'],
    #     # 'streamlit_lightweight_charts_ntf' : ['frontend/yarn.lock','frontend/package.json','frontend/build/index.html'],
    #     # 'streamlit_lightweight_charts_ntf.frontend' : ['streamlit_lightweight_charts_ntf/frontend/build/index.html'],

    #     # '': ['*'],
    #     # 'streamlit_lightweight_charts_ntf.frontend.build.static.js': ['*']
    # },
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.62",
    ],
)
