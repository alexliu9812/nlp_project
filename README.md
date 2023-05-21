# System Installation and Setup Guide

This document provides instructions on how to run the system and set it up properly. Please follow the steps below:

## 1. Clone the project from GitHub 
You can execute the following command:
```
git clone https://github.com/alexliu9812/nlp_project.git
```
## 2. Install PaddlePaddle-GPU package

To begin, you need to install the PaddlePaddle-GPU package. It is crucial to install the correct version based on your operating system and CUDA version. Follow the steps below to install PaddlePaddle-GPU:

For Windows with CUDA version 11.7, run the following command:

```
python -m pip install paddlepaddle-gpu==2.4.2.post117 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
```

For detailed installation instructions, refer to [the official PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html)

Note: Installing the correct version of PaddlePaddle-GPU is crucial for the subsequent deployment. Make sure to choose the appropriate version based on your operating system and CUDA version.

## 3. Install requirements

Next, install the required packages by executing the following command:

```
pip install -r requirements.txt
```


During the installation, you might encounter the following error:

```
RROR: Could not build wheels for hnswlib, which is required to install pyproject.toml-based projects.
```

 This error occurs when Microsoft Visual C++ Build Tools are missing on your computer. You can refer to [the following link](https://stackoverflow.com/questions/73969269/error-could-not-build-wheels-for-hnswlib-which-is-required-to-install-pyprojec) for instructions on how to install them.

## 4. Download model

Download the required models from [Google Drive](https://drive.google.com/drive/folders/1t0ErobEGwqPO8xox3_9EiwklBseOD2fs?usp=share_link) and move them to the `model` folder.

## 5. Run the web application

To start the web application, execute the following command:

```
streamlit run SGenius.py
```

Once the command is executed, the web application will start running.

Thank you for using our system. If you have any further questions or issues, please don't hesitate to contact us.
