# Product Description Generator

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
- Optional integration with DynamoDB for storing generated descriptions.
- Optional S3 storage for archiving requests and responses.
- Serverless deployment using AWS Lambda and API Gateway.

## Architecture

The solution leverages several AWS services:

- **API Gateway**: Exposes RESTful endpoints.
- **AWS Lambda**: Handles API requests and orchestrates generation logic.
- **Amazon Bedrock**: Provides generative AI capabilities.
- **DynamoDB**: Stores generated descriptions.
- **S3**: Archives requests and responses.

