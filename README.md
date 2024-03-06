# 🚀 SCOOP-UI: SHACL Shape Extraction in Just a Click!

This repository demonstrates how to quickly extract and integrate SHACL shapes using SCOOP-UI, a user-friendly web-based interface built with [SCOOP](https://github.com/dtai-kg/SCOOP). With SCOOP-UI, there's no need for complex installations or setups – just click and start shaping your data effortlessly!

### Getting Started

➡️ **Access SCOOP-UI**

Visit our web application at [SCOOP-UI](#) and get started instantly.

### Features

- **Single Resource Input**: When a single source is given as input, e.g., a data schema, an ontology or a set of mapping rules, the application automatically triggers the corresponding shapes extraction component to directly generate the corresponding SHACL shapea.
- **Multiple Resources Inputs**: When multiple resources are given as input, the application invokes the corresponding shape extraction components to extract the shapes and shape integration module to integrate the shapes.
- **Multiple SHACL Shapes Inputs**: While SCOOP is designed to accommodate various input resouces, this application isolates the integration module of SCOOP to enable the support for integrating multiple inputs of SHACL shapes.

### Configurations

- **Integration Strategies**: Select one from three integration strategies: SCOOP-All, SCOOP-Prior, and SCOOP-Prior-R. The adoption of different strategies influences the resolution of conflicting constraints.
- **Integration Priorities**: Easily rearrange and prioritize your SHACL shapes integration using simple drag-and-drop functionality.

### How to Use

1. **Access SCOOP-UI**: Visit the provided URL and start shaping your data immediately.
2. **Input Data**: Enter the text box, upload a file, or click on a predefined example.
3. **Set Configurations**: Click the setting icon next to translate and integrate button. 
4. **Generate Output**: Click the translate and integrate button to generate. 

### Installation Steps incase you want to run locally

- Java Runtime Environment (JRE) - Version 8 or higher
- Python Environment - Version 3.8 or higher

1. **Install Java Runtime Environment (JRE)**:
   - Visit the [Java official website](https://www.java.com/) to download and install the latest version of the Java Runtime Environment (JRE).
   - Once installed, verify that Java is successfully installed by running `java -version` in your command line or terminal.

2. **Install Python Environment**:
   - Visit the [Python official website](https://www.python.org/) to download and install the latest version of Python.
   - After installation, verify that Python is successfully installed by running `python --version` in your command line or terminal.

3. **Install SCOOP-UI**:
   - Download or clone the source code by running `git clone https://github.com/dtai-kg/SCOOP-UI.git`.
   - Navigate to the root directory of SCOOP-UI in your command line or terminal.
   - Run the following command to install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run SCOOP-UI**:
   - Start SCOOP-UI by running the following command in your command line or terminal:
     ```bash
     uvicorn fastapp:app --port 8000 --reload
     ```
   - Open http://localhost:8000/ in your web browser to access SCOOP-UI.

You have now successfully installed and launched SCOOP-UI, and you can start using it!

### Support and Feedback

If you have any questions or feedback, please feel free to open a issue. We're here to help you make the most out of SCOOP-UI.

### License

This project is licensed under the Apache-2.0 license.
