import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import pickle

from io import BytesIO
from flask import Blueprint, Flask, jsonify, make_response, request
from flask_restful  import Resource, Api
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pomegranate import BayesianNetwork

inference_api = Blueprint('inference_api', __name__, url_prefix='/inference')
misclassifications_filename = 'misclassifications.npy'

class ModelGraph(Resource):
    def get(self):
        file = open('red_bayesiana.yml', 'r')
        yaml = file.read()
        file.close()

        model = BayesianNetwork.from_yaml(yaml)

        plt.Figure()
        fig = plt.figure(1, figsize=(20, 20))

        canvas = FigureCanvas(fig)
        fig.suptitle('Red Bayesiana para Prediccion del Glaucoma', fontsize=36)
        model.plot()
        output = BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.headers.set('Content-Type', 'image/png')
        return response


@inference_api.route('/predict', methods=['POST'])
def predict():
    file = open('red_bayesiana.yml', 'r')
    yaml = file.read()
    file.close()

    data = request.get_json()

    values = [
        data['dolor_ocular_severo'],
        data['enrojecimiento_ojo'],
        data['nauseas_vomitos'],
        data['vision_borrosa'],
        data['halos'],
        data['perdida_vision_periferica'],
        data['vision_tunel'],
        data['grupo_edad'],
        data['afroamericano'],
        data['grado_miopia'],
        data['antecedentes_miopia'],
        data['presion_intraocular_mayor_22'],
        data['usa_esteroides'],
        data['diabetes'],
        None
    ]

    model = BayesianNetwork.from_yaml(yaml)

    prediction = model.predict([values])
    probability = model.predict_proba([values])

    result = {
        'prediction': prediction[0][-1],
        'probability': probability[0][-1].parameters
    }

    return jsonify(result)


@inference_api.route('/list_misclassified', methods=['GET'])
def list_misclassified():
    errors = []
    with open(misclassifications_filename, 'rb') as f:
        misclassifications = pickle.loads(f.read())

        for misclassification in misclassifications:

            errors.append(misclassification['consulta'])

        f.close()
    return jsonify(errors)


@inference_api.route('/report_misclassified', methods=['POST'])
def report_misclassified():
    misclassification = request.get_json()

    if os.path.isfile(misclassifications_filename):
        with open(misclassifications_filename, 'rb') as f:
            misclassifications = pickle.loads(f.read())
            f.close()
    else:
        misclassifications = []

    misclassifications.append(misclassification)

    with open(misclassifications_filename, 'wb') as f:
        pickle.dump(misclassifications, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return jsonify({'result': 'ok'})


@inference_api.route('/retrain', methods=['POST'])
def retrain():
    filename = 'misclassifications.npy'
    training_samples = []

    with open(filename, 'rb') as f:
        misclassifications = pickle.loads(f.read())
        f.close()

        for misclassification in misclassifications:
            consulta = misclassification['consulta']
            data = misclassification['criterios']

            training_samples.append([
                data['dolor_ocular_severo'],
                data['enrojecimiento_ojo'],
                data['nauseas_vomitos'],
                data['vision_borrosa'],
                data['halos'],
                data['perdida_vision_periferica'],
                data['vision_tunel'],
                data['grupo_edad'],
                data['afroamericano'],
                data['grado_miopia'],
                data['antecedentes_miopia'],
                data['presion_intraocular_mayor_22'],
                data['usa_esteroides'],
                data['diabetes'],
                '0' if consulta['tiene_glaucoma'] == 'True' else '1'
            ])

    if training_samples:
        df = pd.read_csv('glaucoma_data.csv', '|', dtype=np.str)
        df.head()

        X = df.values
        X = np.vstack((X, np.array(training_samples)))
        model = BayesianNetwork.from_samples(X)
        yaml = model.to_yaml()
        file = open('red_bayesiana.yml', 'w+')
        file.write(yaml)
        file.close()

    with open(filename, 'wb') as f:
        pickle.dump([], f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return jsonify({'result': 'ok'})


def main():
    app = Flask(__name__)
    app.register_blueprint(inference_api)

    api = Api(app)
    api.add_resource(ModelGraph, '/model/graph')

    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
