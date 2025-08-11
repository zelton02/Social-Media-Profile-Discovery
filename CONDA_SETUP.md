### Conda setup for new developers

This guide walks you through setting up and running the project using Conda on macOS, Linux, or Windows.

### Prerequisites

- **Conda**: Install Miniforge, Mambaforge, Miniconda, or Anaconda.
  - Recommended: [Miniforge](https://conda-forge.org/miniforge/)

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd social_media_discovery_project
```

### 2) Create the environment

Using Conda (default):

```bash
conda env create -f environment.yml
```

Using Mamba (faster, optional):

```bash
mamba env create -f environment.yml
```

### 3) Activate the environment

```bash
conda activate social-media-discovery
```

If you prefer not to activate, you can prefix commands with `conda run -n social-media-discovery ...`.

### 4) Configure environment variables (APIFY token)

The script can run without an API token (it will skip external lookups), but to enable real discovery via Apify:

- Option A (recommended): Put your token in `local.env` at the project root.

  Create or edit `local.env` and add:
  ```
  APIFY_API_TOKEN=your_real_token_here
  ```

  The script will auto-load `local.env` if `python-dotenv` is available. If you don’t have it, install it into the env:
  ```bash
  conda install -n social-media-discovery -c conda-forge python-dotenv
  # or
  conda run -n social-media-discovery pip install python-dotenv
  ```

- Option B: Export the token directly in your shell before running:
  - macOS/Linux:
    ```bash
    export APIFY_API_TOKEN=your_real_token_here
    ```
  - Windows (PowerShell):
    ```powershell
    setx APIFY_API_TOKEN "your_real_token_here"
    ```

### 5) Run the script

With the environment activated:

```bash
python social_media_finder.py
```

Or without activation:

```bash
conda run -n social-media-discovery python /Users/zhiheng.ang/personal/social_media_discovery_project/social_media_finder.py
```

Output CSV will be written to `social_media_profiles_updated.csv` in the project root. The input sample used by default is `upload/GankNow-CopyofSampleLeadList-Sheet1.csv`.

### Common tasks

- **Add a package (Conda first preference):**
  ```bash
  conda install -n social-media-discovery -c conda-forge <package>
  ```

- **Add a package (pip inside env):**
  ```bash
  conda run -n social-media-discovery pip install <package>
  ```

- **Export updated environment:**
  ```bash
  conda env export --no-builds | sed '/^prefix: /d' > environment.yml
  ```

- **Remove the environment:**
  ```bash
  conda env remove -n social-media-discovery
  ```

### Troubleshooting

- **conda: command not found**: Ensure Conda is installed and your terminal is configured to initialize Conda (e.g., run `conda init` and restart your shell).
- **Slow solves on Apple Silicon (M-series)**: Prefer Miniforge/Mambaforge or use `mamba` for faster environment creation. The provided `environment.yml` targets `osx-arm64` via conda-forge.
- **Token not detected**: If you’re using `local.env`, make sure `python-dotenv` is installed in the environment, or export `APIFY_API_TOKEN` in your shell.
- **Use the exact environment name**: `social-media-discovery` (from `environment.yml`).

### Notes for IDEs

- In VS Code or similar, select the interpreter from the `social-media-discovery` environment to get linting and intellisense from the correct Python.


