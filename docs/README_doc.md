# 📄 Collaborative LaTeX Project

This directory contains a LaTeX-based document. To ensure consistent builds and avoid local environment issues, we use **Docker** to compile the LaTeX code.

## 📦 Requirements

To build the LaTeX document, make sure you have one of the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- (Optional) [Docker Compose](https://docs.docker.com/compose/install/) – for easier usage

> ⚠️ No need to install LaTeX or any TeX packages on your local machine.

---

## 🚀 Quick Start

### Option 1: Using Docker CLI

```bash
# Build the Docker image
docker build -t latex-builder .
# Compile the LaTeX file (assumes main.tex is the entry point)
docker run --rm -v "$(pwd)":/data latex-builder


```bash
# Build and run the container
docker-compose up --build
