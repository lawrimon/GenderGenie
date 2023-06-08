# GenderGenie

**Author:** Laurin Tarta

## Description

GenderGenie is a web application that utilizes natural language processing techniques to predict whether a german word is gender-neutra. It provides a simple and intuitive interface for users to input text and receive predictions based on a rule based AI

The project consists of a Flask backend, a MongoDB database for storing name data, and a ReactJS frontend for the user interface.

## Technologies Used

- Flask: A micro web framework for the backend development.
- MongoDB: A NoSQL database for storing and retrieving name data.
- ReactJS: A JavaScript library for building user interfaces.

## Features

- Predict if word is gendered.
- User-friendly interface for input and display of text predictions.
- Database integration for storing and retrieving text data.
- Responsive design for seamless user experience across different devices.

## Installation

1. Clone the repository:
git clone https://github.com/lawrimon/GenderGenie.git


2. Set up the backend:
- Navigate to the backend directory:
  ```
  cd GenderGenie/backend
  ```
- Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```
- Start the Flask server:
  ```
  flask run
  ```

3. Set up the frontend:
- Navigate to the frontend directory:
  ```
  cd GenderGenie/frontend
  ```
- Install the required dependencies:
  ```
  npm install
  ```
- Start the React development server:
  ```
  npm start
  ```

4. Access the application in your web browser at http://localhost:3000.

## Usage

1. Enter a text in the provided input field.
2. Click the "Submit" button to generate the gender prediction.
3. The result will be displayed on the screen, indicating the predicted sugestions for the given text.
