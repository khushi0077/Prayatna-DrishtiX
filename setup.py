"""
Setup configuration for DrishtiX Ultimate package.

This allows installation of the package using pip install -e .
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='drishtix-ultimate',
    version='1.0.0',
    description='AI-Powered Wildlife Intrusion Detection System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Prayatna-DrishtiX Team',
    author_email='vikram@example.com',
    url='https://github.com/vikrammm24/Prayatna-DrishtiX',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    keywords='wildlife detection yolov8 opencv ai computer-vision iot',
    project_urls={
        'Bug Reports': 'https://github.com/vikrammm24/Prayatna-DrishtiX/issues',
        'Source': 'https://github.com/vikrammm24/Prayatna-DrishtiX',
        'Documentation': 'https://github.com/vikrammm24/Prayatna-DrishtiX/tree/main/docs',
    },
    entry_points={
        'console_scripts': [
            'drishtix=ai_core.drishtix_main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
