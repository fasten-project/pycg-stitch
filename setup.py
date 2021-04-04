from setuptools import setup, find_packages

def setup_package():
    setup(
        name='pycg-stitch',
        version='0.0.1',
        description='Stitcher for FASTEN Python call graphs',
        license='Apache Software License',
        packages=find_packages(),
        install_requires=[],
        entry_points = {
            'console_scripts': [
                'pycg-stitch=stitcher.__main__:main',
            ],
        },
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3'
        ],
        author = 'Vitalis Salis',
        author_email = 'vitsalis@gmail.com'
    )

if __name__ == '__main__':
    setup_package()
