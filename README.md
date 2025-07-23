# Scout: *Leveraging Large Language Models for Rapid Digital Evidence Discovery*

This tool aims to assist digital forensics investigators by using Large Language Models (LLMs) to perform preliminary evidence processing and prioritization, significantly reducing the time and effort required to sift through large volumes of data.

-----

## 🔍 Overview

In modern legal investigations, the volume of digital evidence is exploding. Forensic investigators are often tasked with analyzing gigabytes or even terabytes of data from various sources like disk images, memory dumps, and network captures. This process is tedious and can lead to significant delays in the justice system.

**Scout** is a framework designed to address this challenge. It employs foundational language models to analyze and identify relevant artifacts from a vast pool of potential evidence. By automating the initial analysis, Scout helps investigators to prioritize their efforts on the most promising pieces of evidence, accelerating the discovery process.

## ✨ Features

  - **🧠 Intelligent Analysis**: Utilizes LLMs to understand the content and context of evidence files, identifying potential artifacts of interest.
  - **📂 Multi-Format Support**: Capable of processing various evidence types, including:
      - **Text-based files**: Emails, documents, logs, and other textual data.
      - **Network Captures**: Analyzes PCAP files to identify suspicious network activity.
      - **Multimedia Files**: Can be extended to analyze images, audio, and video files using multimodal models.
  - **📝 Automated Reporting**: Generates a detailed report of the analysis, summarizing the findings and highlighting key evidence.
  - **🔒 Offline & Secure**: Designed to run in a completely offline, on-premises environment, ensuring the integrity and confidentiality of the evidence. Scout operates in a read-only mode to prevent any tampering.
  - **🧩 Extensible Architecture**: The modular design allows for easy extension with new analysis tools and plugins to support additional file types.

## 🏗️ Architecture

Scout is organized into a modular structure to promote extensibility and maintainability.

```
scout/
├── core/
│   ├── __init__.py
│   ├── agent.py          # The core agent that orchestrates the analysis
│   ├── caller.py         # Handles the execution of external tools
│   └── scout.py          # Main application class
├── prompts/
│   ├── __init__.py
│   ├── system.py         # System prompt for the LLM
│   └── tooluse.py        # Prompt for extracting tool commands
├── utils/
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── helpers.py        # Utility functions
│   └── logger.py         # Logging configuration
├── results/              # Directory for storing analysis reports
├── temp/                 # Temporary directory for scripts and intermediate files
├── __init__.py
├── llm.py                # Wrapper for interacting with the LLM (e.g., Ollama)
├── reporter.py           # Generates the final analysis report
├── requirements.txt      # Project dependencies
├── run.py                # Main entry point for the application
└── summarizer.py         # Summarizes conversation history for the LLM
```

### Key Components

  - **`run.py`**: The main entry point for the Scout application. It handles command-line argument parsing and initializes the analysis process.
  - **`core/agent.py`**: The "brain" of Scout. This agent maintains a conversation with the LLM, determines the next analysis step, and orchestrates the use of various tools.
  - **`core/caller.py`**: A safe interface for executing external tools and shell commands, such as `strings` or other forensic utilities.
  - **`llm.py`**: An interface to the Large Language Model. This implementation uses the `ollama` library to interact with locally hosted models.
  - **`prompts/`**: This directory contains the prompt templates that guide the LLM's behavior, ensuring it acts as a digital forensics assistant.
  - **`reporter.py`**: Responsible for generating the final, human-readable report in Markdown format based on the analysis history.

## 📋 Requirements

  - Python 3.8 or higher
  - [Ollama](https://ollama.ai/) installed and a model downloaded (e.g., `llama3`, `mistral`)
  - Required Python packages (see `requirements.txt`)

## 🚀 Quick Start

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ewre324/Scout-Digital-Forensic-Assistant/
    cd scout
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    

### Usage

The primary way to run Scout is through the `run.py` script. You need to provide the path to the evidence file you want to analyze.

#### Basic Command

```bash
python run.py -e <path_to_evidence_file> --llm-model
```

#### Command Options

  - `--evidence_file`, `-e`: **(Required)** The path to the evidence file to be analyzed.
  - `--llm-model`, `-l`: The name of the Ollama model to use for the analysis. The default is `llama3`.
  - `--max-iterations`, `-m`: The maximum number of analysis iterations (default: 100).
  - `--keep-history`, `-k`: The number of conversation history items to keep in context (default: 14).

#### Examples

  - **Analyze a PCAP file with the default `llama3` model:**

    ```bash
    python run.py -e network_traffic.pcap
    ```

  - **Analyze a disk image using the `mistral` model:**

    ```bash
    python run.py -e suspicious_disk.img --llm-model mistral
    ```

  - **Analyze an email archive with a specific number of history items:**

    ```bash
    python run.py -e enron_emails.mbox -k 20
    ```

## ⚠️ Disclaimer

Scout is intended for **educational and research purposes only**. It is a prototype implementation and should be used as a preliminary analysis tool to assist, not replace, a qualified forensic investigator. Always obtain proper authorization before analyzing any system or data. The authors are not responsible for any misuse of this tool.

## Citation

Please cite  **"Scout: Leveraging Large Language Models for Rapid Digital Evidence Discovery"**
