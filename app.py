from flask import Flask, render_template, request
import funciones as fn

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def upload():
    
    global distancias 
    
    if request.method == 'POST' :

        if request.form.get('upload', True) == 'Subir Archivo de Texto' :

            if request.files['file'] :

                distancias = {}
               
                #Ingresa txt al sistema.
                fn.guardar()
                #Crea Centros.txt y Ventas.txt
                fn.centros_ventas()
                #Distancias entre centros y puntos de venta.
                distancias = fn.distancias()
        
                #Grafica
                fn.aux_graficar()

                #grafoTotalVentas = fn.grafo_pto_ventas()

                return render_template("formulario.html", grafico = True, dict = distancias ) #grafico indica a upload que existe una imagen.
    
            else :
                
                err = 'No se ha seleccionado ningún archivo.'
                
                print(err)
    
        
        if request.form.get("submit", True) == "programar" :
            
            for i in range(len(distancias)) :
                    
                if fn.validar_entrega(request.form["ventas"+str(i+1)], request.form["cantidad"+str(i+1)]) == True : # añadir validaciones

                    print("VALIDACION PASADA")

                else : 

                    print("VALIDACION RECHAZADA")

    return render_template("upload.html")


@app.route("/upload2",methods=["GET","POST"])
def resultados():
    
    if request.method == 'POST':
        
        return "<h1> XD </h1>"


if __name__ == '__main__':
    app.run(debug=True)