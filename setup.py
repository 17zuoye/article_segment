from setuptools import setup

setup(
    name='article_segment',
    version='0.0.2',
    url='http://github.com/17zuoye/article_segment/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='article_segment',
    long_description='article_segment',
    packages=['article_segment'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'wordsegment',
        'split_block',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
