from setuptools import setup, find_packages

setup(name="video_stabilizer",
      version="0.1",
      packages=find_packages(exclude=['tests','tests.*']),
      install_requires=['numpy==1.18.1'],  # TODO: add the rest of the dependencies for the project
      test_suite="tests",
      entry_points={'console_scripts': ['run = video_stabilizer.stabilization_tools.run']}
      )
