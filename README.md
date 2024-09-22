---
title: gg-ai-bot
app_file: gg-ai-bot.py
sdk: gradio
python_version: 3.10.14
sdk_version: 4.44.0
---

# Ollama Chatbot

A basic chatbot designed to help guide my homeschool daughter in English and Math

## Architecture

![Architecture](/architecture.jpg)

## Hugging Face setup

### HuggingFace Initial Setup

```
git remote add space https://huggingface.co/spaces/HF_USERNAME/SPACE_NAME

git push --force space main
```

### Deploy To Huggingface from Terminal

- Get your token from huggingface.co/settings/tokens
- Enable all 3 User permissions: Repositories access (Read and Write)
- The same token will be used in GHA as HF_TOKEN

```
gradio deploy
```

## Run locally

1. Install Python 3.10

```
pyenv install 3.10.14
```

2. Install Poetry
   [from here](https://python-poetry.org/docs/basic-usage/) (I had better experience with brew on MacOS)
3. Create virtual environment for gg-ai-bot (one time)

```
pyenv virtualenv 3.10 gg-bot
```

3. Start virtual environment

```
pyenv shell gg-bot
```

4. Install Dependencies

```
poetry install
```

5. Run application

```
poetry run python gg-ai-bot.py
```

#### Debug

Fetch Debug Configurations

```
poetry debug info
```
