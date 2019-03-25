# Sistema Experto para la Detección del Glaucoma

Se requieren las siguientes librerías para poder integrar con el motor de predicciones:

* numpy
* matplotlib
* pandas
* pomegranate
* pygraphviz
* flask

Para instalar los módulos necesarios se debe ejecutar:

```
pip install numpy
pip install matplotlib
...
```

Por otra parte, el proyecto principal de Google App Engine requiere del módulo __requests__ para poder realizar la comunicación con el motor de predicciones. Para esto se debe instalar __requests__ en el directorio __lib__ del proyecto por medio de:

```
mkdir lib
pip install -r requirements.txt -t lib
```

Para ejecutar el módulo de predicciones se debe ejecutar:

```
python inferencia_flask/inference_api.py
```
