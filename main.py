import yaml
import os
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', default=None)
    parser.add_argument('--yaml_config', default=None)
    args = parser.parse_args()
    
    logdir = args.logdir
    yaml_path = args.yaml_config
    if logdir is None:
        raise RuntimeError("no logdir provided")
    if yaml_path is None:
        yaml_path = os.path.join(logdir, 'run_config.yaml')
        if not os.path.exists(yaml_path):
            raise RuntimeError("no yaml file provided")
    print("yaml path:", yaml_path)
    with open(yaml_path, 'r') as fp:
        yaml_config = yaml.load(fp, Loader=yaml.FullLoader)
    if 'local' in yaml_config and yaml_config['local']:
        stdout_file = open(os.path.join(logdir, 'slurmlog.out'), 'w')
        stderr_file = open(os.path.join(logdir, 'slurmlog.err'), 'w')
        sys.stdout = stdout_file
        sys.stderr = stderr_file
    
    if 'run_type' not in yaml_config:
        raise RuntimeError("No run type in yaml file")
    print("process pid is", os.getpid())    
    # change this and add calls for each run type
    if yaml_config['run_type'] == 'train':
        pass
    else:
        raise RuntimeError("Unknown run type", yaml_config['run_type'])

if __name__ == "__main__":
    main()