from flask import Flask, render_template, request
from flask import flash
from flask_wtf.csrf import CSRFProtect

import forms

app = Flask(__name__)
app.secret_key="clave secreta"

csrf=CSRFProtect()

@app.route("/")
def index():
    titulo = "Flask IDGS801"
    lista = ["Jael", "Juan", "Tristan", "Gibran"]
    return render_template("index.html", titulo=titulo, lista=lista)

@app.route("/operasbas", methods=["GET", "POST"])
def operas1():
    n1 = 0
    n2 = 0
    res = 0
    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        res = float(n1) + float(n2)
    return render_template("operasBas.html", n1=n1, n2=n2, res=res)

@app.route("/resultado", methods=["GET", "POST"])
def resultado():
    n1 = request.form.get('n1')
    n2 = request.form.get('n2')
    tem = float(n1) + float(n2)
    return f"La suma es: {tem}"

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/usuarios",methods=["GET","POST"])
def usuarios():
    mat=0
    nom=''
    apa=''
    ama=''
    email=''
    usuarios_class=forms.UserForm(request.form)
    if request.method=='POST' and usuarios_class.validate():
        mat=usuarios_class.matricula.data
        nom=usuarios_class.nombre.data
        apa=usuarios_class.apaterno.data
        ama=usuarios_class.amaterno.data
        email=usuarios_class.correo.data
        mensaje='Bienvenido {}'.format(nom)
        flash(mensaje)
        
    return render_template("usuarios.html", form=usuarios_class,
                           mat=mat,nom=nom,apa=apa,ama=ama,email=email)

@app.route("/hola")
def hola():
    return "¡Hola, Mundo!"

@app.route("/user/<string:user>")
def user(user):
    return f"Hello, {user}"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {n}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>¡Hola, {username}! Tu ID es: {id}</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"<h1>La suma es_ {n1 + n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>")
def func(param = "juan"):
    return f"<h1>¡Hola, {param}!</h1>"

@app.route("/operas")
def operas():
    return '''
    <form>
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        </br>
        <label for="name">Apellido paterno:</label>
        <input type="text" id="apellido" name="apellido" required>
    </form>
    '''

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    import math
    
    x1 = ''
    y1 = ''
    x2 = ''
    y2 = ''
    distancia_result = 0
    
    if request.method == 'POST':
        x1 = float(request.form.get('x1', 0))
        y1 = float(request.form.get('y1', 0))
        x2 = float(request.form.get('x2', 0))
        y2 = float(request.form.get('y2', 0))
        
        # Calcular la distancia usando la fórmula: d = √((x2-x1)² + (y2-y1)²)
        distancia_result = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return render_template("distancia.html", 
                          x1=x1, y1=y1, x2=x2, y2=y2, 
                          distancia=distancia_result)

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    nombre = ''
    cantidad_compradores = 0
    tiene_tarjeta = False
    cantidad_boletas = 0
    valor_pagar = 0
    mensaje_error = ''
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        cantidad_compradores = int(request.form.get('cantidad_compradores', 0))
        tiene_tarjeta = request.form.get('tarjeta_cineco') == 'si'
        cantidad_boletas = int(request.form.get('cantidad_boletas', 0))
        
        # Validación: máximo 7 boletas por persona
        max_boletas = cantidad_compradores * 7
        
        if cantidad_boletas > max_boletas:
            mensaje_error = f'No se pueden comprar más de {max_boletas} boletas ({cantidad_compradores} persona(s) x 7 boletas)'
        else:
            # Precio base por boleta
            precio_boleta = 12000
            subtotal = cantidad_boletas * precio_boleta
            
            # Aplicar descuento por cantidad de boletas
            descuento_cantidad = 0
            if cantidad_boletas > 5:
                descuento_cantidad = 0.15  # 15%
            elif cantidad_boletas >= 3:
                descuento_cantidad = 0.10  # 10%
            
            total_con_descuento = subtotal * (1 - descuento_cantidad)
            
            # Aplicar descuento adicional por tarjeta CINECO
            if tiene_tarjeta:
                total_con_descuento = total_con_descuento * 0.90  # 10% adicional
            
            valor_pagar = total_con_descuento
    
    return render_template("cinepolis.html", 
                          nombre=nombre,
                          cantidad_compradores=cantidad_compradores,
                          tiene_tarjeta=tiene_tarjeta,
                          cantidad_boletas=cantidad_boletas,
                          valor_pagar=valor_pagar,
                          mensaje_error=mensaje_error)

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True)