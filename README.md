# FastAI FastAPI Image Classification Server

This repository contains a Python server built with FastAPI and FastAI that allows you to predict and classify images using a pre-trained deep learning model. With this server, you can easily deploy your image classification model and make predictions via a user-friendly API.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following requirements installed on your system:

- Python 3.x
- Poetry

#### Will be installed

- FastAPI
- Uvicorn
- FastAI
- PyTorch (usually installed automatically by FastAI)

If you are the using the container , all the above are not required, you can just build the image and run the container

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/DANIELADIKO/test-fast-ai.git
   ```

2. Change into the project directory:

   ```bash
   cd test-fast-ai
   ```
3. Create a new virtual envusing poetry:

   ```bash
   poetry env use <YOUR_PYTHON_VERSION> (python3.11 or above are recommended) 
   ```

4. Install the required Python packages using poetry:

   ```bash
   poetry install 
   ```

## Usage

1. Make sure you have trained a FastAI image classification model and have the model weights saved.

2. Place your trained model weights in the `models` directory.

3. Start the FastAPI server using Uvicorn:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   - `--host 0.0.0.0` allows the server to accept external connections.
   - `--port 8000` specifies the port on which the server will run.

4. Your server is now running! You can access the API by navigating to `http://localhost:8000` in your web browser or using an API client like [Postman](https://www.postman.com/).

## API Documentation

### Predict Image

Endpoint: `/predict`

- **HTTP Method**: POST

#### Request

- **Body**: Multipart form data with a file field named `image`.

#### Response

- **Status Code**: 200 OK
- **Body**: JSON response with the predicted class and confidence score.

#### Example Request

```bash
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:8000/predict
```

#### Example Response

```json
{
  "class": "cat",
  "confidence": 0.987
}
```

## Deployment

To deploy this FastAI FastAPI server in a production environment, you can use various hosting providers like AWS, Google Cloud, or Heroku. Be sure to configure environment variables and security settings according to best practices for your chosen deployment platform.

## Contributing

Contributions to this project are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md) when making pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.