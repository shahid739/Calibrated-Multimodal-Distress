from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dersx",
    version="1.0.0",
    author="Muhammad Shahid, Humera Arshad",
    author_email="f23bdocs4m01004@iub.edu.pk",
    description="DERS-X: Calibrated Multimodal Distress-Like Affect Modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shahid739/Calibrated-Multimodal-Distress",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "transformers>=4.30.0",
        "datasets>=2.12.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.2.0",
        "matplotlib>=3.7.0",
        "tqdm>=4.65.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "flake8>=6.0.0"],
        "interp": ["captum>=0.6.0"],
    },
)