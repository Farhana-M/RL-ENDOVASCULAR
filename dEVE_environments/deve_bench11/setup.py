from setuptools import setup, find_packages

setup(
    name="eve_bench11",
    version="0.0",
    packages=find_packages(),
    package_data={
        'eve_bench11': [
            'aorticarch/arch_vmr94_util/*.stl',  # STL files under aorticarch
            'mesh_full/*.obj',  # OBJ files directly under mesh_full
            'mesh_full/*.json',  # JSON files directly under mesh_full
            'mesh_full/Centrelines_comb/*.*',  # All files under Centrelines_comb
        ],
    },
    include_package_data=True,
    install_requires=[
        "numpy", "pillow", "scipy", "scikit-image", "pyvista", "meshio", 
        "PyOpenGL", "pygame", "matplotlib", "opencv-python",
    ],
)
