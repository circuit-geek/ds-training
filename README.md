* This project uses a different python package manager called `uv` which is much faster than pip and can
  handle all your python packages with versioning too.
* If you don't have uv installed in your system first run the below command in powershell: <br />
    `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
* Confirm the installation by restarting the powershell and by running `uv --version` (You shouldn't get any error here)
* Firstly, clone this repository in your local system by using the following command: <br />
    `git clone https://github.com/circuit-geek/ds-training.git` <br />
    `cd ds-training` <br />
    `uv sync`
* To run the files you can use the command `uv run python_file_name` or if your using any IDE you can run it inside it.
