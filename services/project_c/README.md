# New Project Template

This directory is a template for adding new projects to the `project-integrator`.

## How to Add a New Project

1.  **Copy the Template**: Copy this entire `project_template` directory and rename it to your new project's name (e.g., `project_c`).

    ```bash
    cp -r services/project_template services/project_c
    ```

2.  **Develop Your Code**:
    *   Place your Python code in the new directory (`services/project_c`).
    *   The main entry point for your project must be a file named `main.py`.
    *   Add any Python dependencies for your project to the `requirements.txt` file. The GitHub Actions workflow will automatically install them.

3.  **Update Configuration**:
    *   Open the main `config.json` file in the root of the `project-integrator` repository.
    *   Add your new project as a new object under the `services` key.

    ```json
    {
      "services": {
        "project_a": {
          "path": "services/project_a",
          "config_file": "config.py",
          "description": "Project-Automate のコードを格納"
        },
        "project_b": {
          "path": "services/project_b",
          "config_file": "config.py",
          "description": "Project-Progress-Manager のコードを格納"
        },
        "project_c": {
          "path": "services/project_c",
          "config_file": "config.py",
          "description": "Description for your new project"
        }
      },
      "slack": {
        "webhook_url": "...",
        "channel": "...",
        "notify_on_start": true,
        "notify_on_finish": true
      },
      "dashboard": {
        "output_path": "..."
      },
      "logging": {
        "log_dir": "...",
        "log_file": "...",
        "level": "INFO"
      }
    }
    ```

4.  **Run and Test**:
    *   The `run_all.py` script will now automatically pick up and run your new project in the sequence defined by the `config.json`.
    *   When you push your changes to the `main` branch, the GitHub Actions workflow will also run your project as part of the integration.

## Development Workflow

The recommended development workflow is:

1.  **Design**: Discuss the project design with a large language model like ChatGPT-5 to create a blueprint.
2.  **Develop**: Use an AI software engineer like Jules to develop and test the code within the GitHub environment.
3.  **Integrate**: Add the new project to this `project-integrator` repository following the steps above.
4.  **Verify**: Test the integrated execution using `run_all.py` or by pushing to GitHub.
5.  **Review**: Check the results of the execution in Notion, Slack, or other dashboards.
