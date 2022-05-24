from setuptools import setup, find_packages

def get_long_desc():
    with open("pypi-readme.md", "r") as readme:
        desc = readme.read()

    return desc

def setup_package():
    setup(
        name='pycg-stitch',
        version='0.0.8',
        description='Stitcher for FASTEN Python call graphs',
        long_description=get_long_desc(),
        long_description_content_type="text/markdown",
         url='https://github.com/fasten-project/pycg-stitch',
        license='Apache Software License',
        packages=find_packages(),
        install_requires=['flask'],
        include_package_data=True,
        entry_points = {
            'console_scripts': [
                'pycg-stitch=stitcher.__main__:main',
            ],
        },
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3'
        ],
        author = 'Vitalis Salis, Giorgos Drosos',
        author_email = 'vitsalis@gmail.com, drosos007@gmail.com'
    )

if __name__ == '__main__':
    setup_package()
