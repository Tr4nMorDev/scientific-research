from setuptools import setup, find_packages

setup(
    name="vehicle_detection",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-SocketIO',
        'Flask-Cors',
        'python-dotenv',
        'pytest',
    ],
) 