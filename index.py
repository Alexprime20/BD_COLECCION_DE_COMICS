from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="tienda"
MONGO_COLECCION="Comics"


cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]


# MOSTRAR DATOS
def mostrarDatos():

    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)        
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"],value=(documento["title"], documento["author"], documento["publicationDate"], documento["genre"], documento["description"]))  
        
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido"+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb"+errorConexion)      
      
# CREAR REGISTRO
def crearRegistro():
    if len(Titulo.get())!=0 and len(Autor.get())!=0 and len(Fecha.get())!=0 and len(Genero.get())!=0 and len(Descripcion.get())!=0:
        
        try:
            documento={"title":Titulo.get(),"author":Autor.get(),"publicationDate":Fecha.get(),"genre":Genero.get(),"description":Descripcion.get()} 
            coleccion.insert_one(documento)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    
    mostrarDatos()
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"]) 
    #print(ID_ALUMNO)
    documento=coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    #print(documento)
    Titulo.delete(0,END)
    Titulo.insert(0,documento["title"])
    Autor.delete(0,END)
    Autor.insert(0,documento["author"]) 
    Fecha.delete(0,END)
    Fecha.insert(0,documento["publicationDate"]) 
    Genero.delete(0,END)
    Genero.insert(0,documento["genre"]) 
    Descripcion.delete(0,END)
    Descripcion.insert(0,documento["description"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"
            
#tabla
def editarRegistro():

    global ID_ALUMNO

    if len(Titulo.get())!=0 and len(Autor.get())!=0 and len(Fecha.get())!=0 and len(Genero.get())!=0 and len(Descripcion.get())!=0:
        try:
            idbuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosvalores={"$set":{"title":Titulo.get(),"author":Autor.get(),"publicationDate":Fecha.get(),"genre":Genero.get(),"description":Descripcion.get()} } 
            coleccion.update_one(idbuscar,nuevosvalores)
            Titulo.delete(0,END)
            Autor.delete(0,END)
            Fecha.delete(0,END)
            Genero.delete(0,END)
            Descripcion.delete(0,END)

        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()    
        
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"     

def borrarRegistro():
    
    global ID_ALUMNO
    
    try:
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        coleccion.delete_one(idBuscar)
        Titulo.delete(0,END)
        Autor.delete(0,END)
        Fecha.delete(0,END)
        Genero.delete(0,END)
        Descripcion.delete(0,END)
    
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"    
    mostrarDatos()


ventana=Tk()
columnas = ('#0', '#1', '#2', '#3', '#4')
tabla = ttk.Treeview(ventana, columns=columnas)
tabla.grid(row=1, column=0,columnspan=3 )
tabla.heading("#0",text="ID")
tabla.heading("#1",text="Titulo")
tabla.heading("#2",text="Autor")
tabla.heading("#3",text="Fecha-Publicacion")
tabla.heading("#4",text="Genero")
tabla.heading("#5",text="Descripcion")
tabla.bind("<Double-Button-1>",dobleClickTabla)


#campos 
Label(ventana,text="titulo").grid(row=2, column=0)
Titulo=Entry(ventana)
Titulo.grid(row=2,column=1)
Label(ventana,text="Autor").grid(row=3, column=0)
Autor=Entry(ventana)
Autor.grid(row=3,column=1)
Label(ventana,text="Fhecha-Publicacion").grid(row=4, column=0)
Fecha=Entry(ventana)
Fecha.grid(row=4,column=1)
Label(ventana,text="Genero").grid(row=5, column=0)
Genero=Entry(ventana)
Genero.grid(row=5,column=1)
Label(ventana,text="Descripcion").grid(row=6, column=0)
Descripcion=Entry(ventana)
Descripcion.grid(row=6,column=1)

#Boton Crear
crear=Button(ventana,text="Ingresar",command=crearRegistro,bg="green",fg="white")
crear.grid(row=7, columnspan=2)

#Boton Editar
editar=Button(ventana,text="Editar",command=editarRegistro,bg="yellow")
editar.grid(row=8,columnspan=2)
editar["state"]="disabled"

#boton Borrar
borrar=Button(ventana,text="Eliminar",command=borrarRegistro,bg="red",fg="green")
borrar.grid(row=9,columnspan=2)
borrar["state"]="disabled"



mostrarDatos()
ventana.mainloop()
