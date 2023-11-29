import optuna
import yaml
from config_reader import ConfigReader
import models.classification.models as clas
import models.regression as regr
from models import ModelFactory
from sklearn.model_selection import train_test_split
from sklearn import datasets
from models import ModelFactory
from optimization.init import TuneFactory
from sklearn.metrics import accuracy_score

#config_name="config/config_svm.yml"
config_name="config/config_rand_for.yml"


config_file = ConfigReader(config_name)
optim_infos = config_file.get_optimization_info()
model_info = config_file.get_model_info()
parameters_infos = config_file.get_parameter_ranges_bayes()
print(parameters_infos)
data_infos = config_file.get_data_paths()

optim_method = optim_infos["method"]
model_name = model_info["name"]
prob_type = model_info["problem_type"]

iris = datasets.load_iris()
X, y = iris.data[:, :2], iris.target
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3, random_state=42)

if __name__ == "__main__":

    model = ModelFactory.create_model(prob_type, model_name)
    optim_model = TuneFactory.create_model(optim_method)
    bayesian_search = optim_model.tune(model.model, parameters_infos, X_train, y_train, X_valid, y_valid)
    print(f"Best Parameters:")
    print(optim_model.get_best_params(bayesian_search))
    best_model = optim_model.fit_best_model(bayesian_search, X_train, y_train)
    y_pred = optim_model.predict_result(best_model, X_valid)
    print("Tuned accuracy:")
    print(accuracy_score(y_valid, y_pred))

    model_ = ModelFactory.create_model(prob_type, model_name)
    model_.train(X_train, y_train)
    print("Non Tuned accuracy:")
    print(model_.accuracy(X_valid, y_valid))
