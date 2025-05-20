import os
import yaml
from datetime import datetime
import argparse
import copy
import subprocess


# Change here to your user
DEFAULT_LOG_DIR = '/vol/scratch/USER/runs'

def submit_task(config: dict, args:argparse.Namespace):
    config = copy.deepcopy(config)
    slurm_config = config['slurm_params']
    
    if 'logdir' in config:
        logdir_base = config['logdir']
    else:
        logdir_base = DEFAULT_LOG_DIR
    run_name = f"{datetime.now().strftime('%y%m%d-%H%M%S')}_{config['run_name']}"
    logdir = os.path.join(logdir_base, run_name) # ckpts and midi will be saved here
    cmd = ['sbatch', f'--export=ALL,LOGDIR={logdir}']

    config['logdir'] = logdir
    slurm_config['output'] = os.path.join(logdir, slurm_config['output'])
    slurm_config['error'] = os.path.join(logdir, slurm_config['error'])
    os.makedirs(logdir, exist_ok=True)
    new_yaml_path = os.path.join(logdir, 'run_config.yaml')
    with open(new_yaml_path, 'w') as fp:
        yaml.dump(config, fp)

    
    for opt, val in slurm_config.items():
        cmd.extend([f'--{opt}', str(val)])
        
    cmd.extend([config['command'], '--logdir', logdir, '--yaml_config', new_yaml_path])
    local_command = f"python3 main.py --logdir {logdir} --yaml_config {new_yaml_path}"
    if 'local' in config and config['local']:
        os.system(local_command)
    else:
        if args.dry_run:
            print(' '.join(cmd))
            return
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        job_id = result.stdout.strip().split()[-1]
        with open(os.path.join(logdir, 'job_launch.log'), 'a') as f:
            f.write("Job ID: " + job_id + '\n')
        print("Submitted SLURM job:", job_id)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit a SLURM job or run a task locally based on a YAML config.")
    parser.add_argument('--yaml_config', default='config.yaml')
    parser.add_argument('--dry_run', action='store_true',
                    help="Print sbatch command instead of executing")

    args = parser.parse_args()
    with open(args.yaml_config, 'r') as fp:
        config = yaml.safe_load(fp)
        
    submit_task(config, args)
   
            