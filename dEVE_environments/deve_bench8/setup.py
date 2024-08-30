from setuptools import setup, find_packages
from glob import glob

visu_mesh_data = glob("eve_bench8/aorticarch/arch_vmr94_util/*.stl")
setup(
    name="eve_bench8",
    version="0.0",
    packages=find_packages(),
    data_files=[
        (
            "visu_mesh_data",
            visu_mesh_data,
        ),
    ],
    include_package_data=True,
    install_requires=[
        "numpy",
        "pillow",
        "scipy",
        "scikit-image",
        "pyvista",
        "meshio",
        "PyOpenGL",
        "pygame",
        # "pyqt5",
        "matplotlib",
        "opencv-python",
    ],
)
