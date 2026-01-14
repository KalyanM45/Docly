# Doclify 📚

**Doclify** is an intelligent command-line tool that automates the process of documenting your software projects. By leveraging the power of **Google's Gemini LLMs**, Doclify scans your codebase, understands the context of each file, and generates a comprehensive, professional `README.md` file.

> **Note:** This project was formerly known as `docly`.

## ✨ Key Features

- **🚀 Two-Stage Generation**: verification-driven documentation that first analyzes individual files for granule details, then aggregates them into a holistic project summary.
- **🤖 Powered by Gemini**: Uses the latest `google-genai` SDK to provide accurate code summaries and architecture explanations.
- **⚡ Smart Scanning**: Automatically respects your `.gitignore` rules to only document what matters.
- **🎨 Beautiful CLI**: Features a polished terminal interface with progress bars, spinners, and clean logs using the `rich` library.
- **🛡️ Safety First**: Never overwrites your work without a backup. Doclify automatically saves your existing `README.md` to `README-prev.md` before generating a new one.
- **⚙️ Configurable**: Fully customizable via `doclify.yaml`.

## 📦 Installation

You can install Doclify directly from PyPI (once published) or build it locally.

### Local Development
```bash
git clone https://github.com/yourusername/doclify.git
cd doclify
pip install -e .
```

## 🛠️ Configuration

Doclify requires a Google API Key to function. You must set this environment variable before running the tool.

**Windows (CMD)**:
```cmd
set GOOGLE_API_KEY=your_actual_api_key_here
```

**Windows (PowerShell)**:
```powershell
$env:GOOGLE_API_KEY="your_actual_api_key_here"
```

**Linux/macOS**:
```bash
export GOOGLE_API_KEY=your_actual_api_key_here
```

## 🚀 Usage

Using Doclify is a simple two-step process:

### 1. Initialize
Run the init command to scan your directory and create a configuration file (`doclify.yaml`). This file lists all the source files that will be analyzed.

```bash
doclify init
```

### 2. Generate
Run the main command to analyze your code and generate the documentation.

```bash
doclify run
```

Once complete, you will see a new `README.md` in your project root!

## 🤝 Contributing

Contributions are welcome!
1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Open a Pull Request.

## 📄 License

[MIT License](LICENSE)
