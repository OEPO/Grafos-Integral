from flask import Flask, render_template, request
import funciones as fn

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload",methods=["POST"])
def upload():
    if request.method == 'POST':

        #Ingresa txt al sistema.
        fn.guardar()
        #Crea Centros.txt y Ventas.txt
        fn.centros_ventas()
        #Distancias entre centros y puntos de venta.
        distancias = fn.distancias()
        
        #Grafica
        fn.aux_graficar()

        return render_template("upload2.html", grafico = True, dict = distancias) #grafico indica a upload que existe una imagen.
    else:
        return render_template("upload.html")

@app.route("/upload2",methods=["POST"])
def resultados():
    if request.method == 'POST':
        return "<h1>Resultados</h1>"

if __name__ == '__main__':
    app.run(debug=True)