# slurm_tasks

## To-do List

1. Set your base log directory path in `send_to_slurm.py` (`DEFAULT_LOG_DIR`).
2. Set your task parameters and command to run in `config.yaml` or any other YAML file.
3. Change the virtual environment path inside 'run_main'

## How to Run

```bash
python send_to_slurm.py --yaml_config YAML_PATH

note that you need pyaml for this so you might need to activate your virtual environment first
