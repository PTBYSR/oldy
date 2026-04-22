<p align="center">
  <img src="oldy-hero.png" alt="Oldy Header" width="600">
</p>

# Oldy

Turn any old laptop into a local AI server.

## What it does

Install Oldy on a low-RAM laptop. It detects your hardware, picks a model that fits,
starts a local AI server, and gives you a public URL you can hit from anywhere.

## Requirements

- Python 3.10+
- Linux or macOS
- 4GB+ RAM

## Install

pip install oldy

## Usage

oldy start      # detect hardware, pick model, start server, get public URL
oldy stop       # shut everything down
oldy status     # RAM, CPU, uptime, current model
oldy models     # browse and switch models
oldy logs       # live request log
oldy url        # print your public URL

## How it works

[architecture diagram image here — add after recording demo]

Oldy manages Ollama under the hood. You never touch Ollama directly.
An ngrok tunnel makes your local server publicly accessible without
port forwarding or networking setup.

## Supported models (v1)

| Model            | Size   | Min RAM |
|------------------|--------|---------|
| tinyllama        | 0.6GB  | 1GB     |
| qwen2:1.5b       | 0.9GB  | 2GB     |
| deepseek-r1:1.5b | 1.1GB  | 2GB     |
| gemma:2b         | 1.5GB  | 3GB     |
| llama3.2:3b      | 2.0GB  | 3GB     |
| phi3:mini        | 2.3GB  | 4GB     |
| mistral:7b       | 4.1GB  | 6GB     |

## Demo

[add GIF here]
