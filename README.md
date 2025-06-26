# AI Product Description Generator

[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/product-description-generator/ci.yml?branch=main)](https://github.com/your-org/product-description-generator/actions)
[![Test Coverage](https://img.shields.io/codecov/c/github/your-org/product-description-generator/main.svg)](https://codecov.io/gh/your-org/product-description-generator)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting up the Python Environment](#setting-up-the-python-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [AWS Configuration](#aws-configuration)
- [Deployment](#deployment)
- [Usage](#usage)
  - [API Endpoint](#api-endpoint)
  - [Example Request](#example-request)
  - [Example Response](#example-response)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

**Product Description Generator** is an AWS-powered API that generates compelling product descriptions using Amazon Bedrock's generative AI models. It aims to automate and streamline the creation of both short and detailed product descriptions for e-commerce, marketing, and catalog management.

## Features

- Generate short or detailed product descriptions via API.
- Utilizes Amazon Bedrock for high-quality AI-generated text.
- Integration with DynamoDB for storing generated descriptions.
- S3 storage for archiving requests and responses.
- Serverless deployment using AWS Lambda and API Gateway.

## Architecture

The solution leverages several AWS services:

- **API Gateway**: Exposes RESTful endpoints.
- **AWS Lambda**: Handles API requests and orchestrates generation logic.
- **Amazon Bedrock**: Provides generative AI capabilities.
- **DynamoDB**: Stores generated descriptions.
- **S3**: Archives requests and responses.

## Setup & Installation

### Prerequisites

- Python 3.9+
- AWS CLI
- AWS SAM CLI
- Git

### Cloning the Repository

```sh
git clone https://github.com/your-org/product-description-generator.git
cd product-description-generator
```

### Setting up the Python Environment

- Using venv:
```sh
python3 -m venv .venv
source .venv/bin/activate
```
- Installing Dependencies
```sh
pip install -r requirements.txt
```

### AWS Configuration

```sh
aws configure
```

### Deployment

- Build and deploy the application using AWS SAM:
```sh
sam build
sam deploy --guided
```

### Usage

- API Endpoint
After deployment, note the API Gateway endpoint URL from the SAM output.

- Example Request
POST /generate
```sh
{
  "product_name": "Eco-Friendly Water Bottle",
  "features": ["BPA-free", "Reusable", "Insulated"],
  "description_type": "detailed"
}
```
- Example Response
```sh
{
  "description": "Introducing the Eco-Friendly Water Bottle: BPA-free, reusable, and insulated to keep your drinks at the perfect temperature. Ideal for those who care about the environment and want a reliable hydration solution."
}
```