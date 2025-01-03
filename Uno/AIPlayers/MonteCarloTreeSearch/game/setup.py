# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="CGameSimulation",  # Nazwa modułu
        sources=["CGameSimulation.pyx"],  # Ścieżka do pliku .pyx w tym samym folderze
        # Możesz dodać inne opcje, takie jak include_dirs, libraries, library_dirs, jeśli potrzebne
    )
]

setup(
    name="CGameSimulation",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
