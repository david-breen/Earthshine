from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Ground Based Earthshine Measurements'
LONG_DESCRIPTION = '''Tools and code for the Earthshine cubesat ground based
                      tests'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="EarthshineMeasurement", 
        version=VERSION,
        author="David Breen",
        author_email="<david.breen@maine.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'numpy',
            'cv2',
            'matplotlib'
        ], # add any additional packages that
        # needs to be installed along with your package.
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)