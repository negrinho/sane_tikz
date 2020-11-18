from setuptools import setup, find_packages

setup(name='sane_tikz',
      version='0.1',
      description='Python to TikZ transpiler',
      long_description=open('tutorial.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      url='http://github.com/negrinho/sane_tikz',
      author='Renato Negrinho',
      author_email='renato.negrinho@gmail.com',
      license='MIT',
      packages=find_packages(include=["sane_tikz*"]),
      python_requires='>=3.6',
      install_requires=["numpy"],
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          "Topic :: Scientific/Engineering :: Visualization"
      ])