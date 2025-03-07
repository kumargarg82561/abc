# Diabetes Prediction Model

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

This repository contains the source code and implementation for a liver disease prediction model deployed on Flask. The machine learning model predicts the likelihood of liver disease based on input features such as age, gender, various health metrics, and test results.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- Flask web application for liver disease prediction
- Pre-trained machine learning model
- User-friendly web interface
- Input validation and error handling
- Complete backend integration
- Complete database integration

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/XDFrost/SafeInsights-Diabetes-Prediction-Model-based-on-flask.git
   ```
   
2. Change into the project directory:

   ```bash
   cd SafeInsights-Diabetes-Prediction-Model-based-on-flask
   ```
   
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Add uri and app passwords to config.json file. Make a .env file and add variables in it
   
   Required variables for .env file:

      1. production_URI
      2. secret_key
      3. MAIL_USERNAME
      4. MAIL_PASSWORD

3. Start the Flask application:

   ```bash
   python app.py
   ```
   
4. Open your web browser and go to [http://localhost:5000](http://localhost:5000)

5. Use the web interface to input the required features and get predictions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
