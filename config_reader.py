import yaml
import numpy as np
import optuna

class ConfigReader:
    def __init__(self, config_file):
        with open(config_file, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    def read(self):
        return self.config

    def get_model_info(self):
        model_info = {
            'name': self.config['model']['name'],
            'problem_type': self.config['model']['problem_type'],
        }
        return model_info
    
    def get_optimization_params(self):
        optimization_params = {
            'cv': self.config['optimization']['cv'],
            'verbose': self.config['optimization']['verbose'],
            'n_iter': self.config['optimization']['n_iter'],
            'n_jobs': self.config['optimization']['n_jobs'],
            'random_state': self.config['optimization']['random_state'],
            'n_trials': self.config['optimization']['n_trials'],
            'timeout': self.config['optimization']['timeout'],
            'show_progress_bar': self.config['optimization']['show_progress_bar']
        }
        return optimization_params

    def get_data_paths(self):
        data_paths = {
            'train_path': self.config['data']['train_path'],
            'test_path': self.config['data']['test_path']
        }
        return data_paths

    def get_parameter_ranges(self, optim_method, trial=None):
        parameter_ranges = {}
        if optim_method in ["grid_search", "random_search"]:
            for param, param_info in self.config['model']['parameters'].items():
                suggest_type = param_info['suggest_type']
                if suggest_type in ["suggest_float"]:
                    min_, max_ = float(param_info['min']), float(param_info['max'])
                    parameter_ranges[param] = np.linspace(min_, max_, 10)
                elif suggest_type in ["suggest_int"]:
                    min_, max_ = int(param_info['min']), int(param_info['max'])
                    parameter_ranges[param] = [int(x) for x in np.linspace(min_, max_, 20)]
                elif suggest_type == 'suggest_categorical':
                    parameter_ranges[param] = param_info['choices']
                else:
                    raise ValueError(f"Unknown suggest_type: {suggest_type}")
        elif optim_method == "bayesian_optim":
            for param, param_info in self.config['model']['parameters'].items():
                suggest_type = param_info['suggest_type']
                if suggest_type in ["suggest_float"]:
                    parameter_ranges[param] = (float(param_info['min']), float(param_info['max']))
                elif suggest_type in ["suggest_int"]:
                    parameter_ranges[param] = (int(param_info['min']), int(param_info['max']))
                elif suggest_type == 'suggest_categorical':
                    parameter_ranges[param] = param_info['choices']
                else:
                    raise ValueError(f"Unknown suggest_type: {suggest_type}")
        elif optim_method == "optuna":
            for param, param_info in self.config['model']['parameters'].items():
                suggest_type = param_info['suggest_type']
                if suggest_type in ["suggest_float"]:
                    parameter_ranges[param] = (float(param_info['min']), float(param_info['max']), suggest_type)
                elif suggest_type in ["suggest_int"]:
                    parameter_ranges[param] = (int(param_info['min']), int(param_info['max']), suggest_type)
                elif suggest_type == 'suggest_categorical':
                    parameter_ranges[param] = [param_info['choices'], suggest_type]
                else:
                    raise ValueError(f"Unknown suggest_type: {suggest_type}")
        return parameter_ranges