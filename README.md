
# Shape and Shade 

The **Hair Style Recommendation System Based On Face Shape** is an AI-powered Flask web application designed to deliver personalized hair styling recommendations based on an individual's unique facial structure.

By combining computer vision algorithms with deep learning models, the system analyzes facial landmarks and skin undertones from an uploaded image or real-time webcam feed to suggest flattering haircuts, styles, and hair dye shades tailored to each user.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)

## Overview
Overview Here

## Project Structure

```text
shape_and_shade_project/
|── .venv/                   # Virtual environment (ignored by git)
|── app/                     # App
|   |── static/              # Public assets (CSS, JavaScript, Images)
│   |    |── css/            # Stylesheet 
│   |    │   └── style.css
|   |    ├── js/             # JavaScript
|   |        └── main.js
|   └── templates/           # Jinja2 HTML templates
|        └── index.html      # Primary application view
|── main.py                  # Application entry point and routes
|── requirements.txt         # Dependency list
|── .gitignore               # Git ignore settings
└── README.md                # Project documentation
```

## Prerequisites
Before starting, ensure you have the following installed on your machine:

- Python 3.10+ (Python 3.11 or 3.12 recommended)

- pip (Python Package Installer)

- Git

**Verify your Python installation by running**:

```
python3 --version
```
or 
```
python --version
```

**Verify your Git installation by running**:
```
git --version
```

## Installation & Setup
1. Clone the Repository
```
git clone git@github.com:KhantKhantWinTintt/shape_and_shade_project.git

```
```
cd shape_and_shade_project
```
2. Create a Virtual Environment

- macOS / Linux:
```
python3 -m venv .venv
```
- Windows:
```
python -m venv .venv
```
3. Activate the virtual environment
- macOS / Linux
```
source .venv/bin/activate 
```
- Windows:
```
.venv\Scripts\activate
```
4. Upgrade Build Tool
```
python -m pip install --upgrade pip
```
5. Install Required Packages
```
pip install -r requirements.txt
```

## Running the Application
```
python main.py
```
- Accessing the web app
```
http://127.0.0.1:5000
```
