from setuptools import setup,find_packages

setup(
    name="query",
    version="0.1",
    description="使用sql处理pandas数据",
    author='liu.xin',
    author_email="1627094964@qq.com",
    packages=find_packages('.',['./query/__pycache__']),
    install_requires = [
        'pandas'
    ],
    test_requires=[
        'pytest'
    ]
)