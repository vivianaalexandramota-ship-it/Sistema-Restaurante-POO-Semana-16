# Sistema Restaurante POO - Semana 16

## Propósito
Esta versión corresponde a la **Semana 16 de Programación Orientada a Objetos**. Es una evolución directa del proyecto de la Semana 15: conserva el inicio de sesión, la gestión de productos, el registro de ventas, la persistencia mediante archivos JSON, la arquitectura modular y los recursos visuales de `assets/`.

La evolución principal de esta semana es la **gestión administrativa de usuarios basada en eventos de Tkinter**, utilizando `Treeview`, `Combobox`, `bind()`, callbacks y atajos de teclado.

## Evolución realizada
La sección **Usuarios** fue ampliada para permitir que un usuario con rol **Administrador** pueda:

- Registrar usuarios.
- Consultar usuarios en una tabla `Treeview`.
- Seleccionar un usuario y cargar sus datos en el formulario.
- Actualizar usuarios de tipo **Empleado** o **Cliente**.
- Eliminar usuarios de tipo **Empleado** o **Cliente** con confirmación previa.
- Limpiar el formulario y cancelar la selección actual.

Se incorporaron los tres roles solicitados:

- `Administrador`
- `Empleado`
- `Cliente`

El acceso a la pestaña administrativa de usuarios está disponible únicamente para el rol **Administrador**. La cuenta Administrador está protegida para evitar su modificación o eliminación accidental desde la gestión de usuarios.

## Arquitectura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── icon.png
│   └── logo.png
└── main.py
```

La organización separa responsabilidades:

- **modelos/** representa los datos del sistema.
- **servicios/** contiene validaciones, reglas de negocio y persistencia.
- **ui/** contiene la interfaz y responde a las interacciones del usuario.
- **datos/** almacena la persistencia en JSON.
- **assets/** almacena el logo, icono y recursos visuales.
- **main.py** es el punto de entrada de la aplicación.

## Gestión de usuarios y persistencia
El modelo `Usuario` incluye el atributo `rol`. Los usuarios se almacenan en `datos/usuarios.json`.

La interfaz **no lee ni escribe JSON directamente**. Todas las operaciones de usuarios se delegan a `RestauranteServicio`, que se encarga de:

- `listar_usuarios()`
- `buscar_usuario()`
- `registrar_usuario()`
- `actualizar_usuario()`
- `eliminar_usuario()`
- `validar_acceso()`

También se valida que no existan nombres de usuario duplicados y que los datos requeridos sean válidos.

## Eventos implementados en Semana 16

### `<<TreeviewSelect>>`
Se asocia mediante `bind()` a la tabla de usuarios. Al seleccionar una fila, la interfaz obtiene únicamente el **ID** mostrado en la tabla y solicita el objeto completo a `RestauranteServicio`. De esta forma no se almacena información sensible como la contraseña dentro del `Treeview`.

Flujo:

```text
selección de fila
→ <<TreeviewSelect>>
→ bind()
→ callback(event)
→ obtener ID
→ RestauranteServicio.buscar_usuario()
→ cargar formulario
```

### `<Return>`
Se utiliza como atajo para registrar un usuario desde el formulario. El callback del evento reutiliza el mismo método `_callback_registrar_usuario()` que utiliza el botón **Registrar**, evitando duplicar lógica.

### `<Escape>`
Limpia el formulario, cancela la selección del `Treeview` y devuelve la gestión de usuarios a su estado inicial.

### `<<ComboboxSelected>>`
Se aplica al `Combobox` de roles para responder visualmente cuando el administrador selecciona **Empleado** o **Cliente**.

## Diferencia entre `bind()` y `command=`

- `bind()` se utiliza para asociar eventos de teclado o eventos virtuales de widgets con callbacks que reciben un parámetro `event`.
- `command=` se mantiene en los botones **Registrar**, **Actualizar**, **Eliminar** y **Limpiar**, tal como solicita la actividad.

Los callbacks coordinan la interacción y actualizan la vista, pero la lógica de validación y persistencia permanece en `RestauranteServicio`.

## Funciones conservadas de semanas anteriores

- Inicio de sesión mediante `usuarios.json`.
- Gestión de productos: registrar, consultar, actualizar y eliminar.
- Persistencia de productos en `productos.json`.
- Registro de ventas relacionando usuario y producto.
- Persistencia de ventas en `ventas.json`.
- Visualización de ventas en `Treeview`.
- Logo e icono cargados desde `assets/`.

## Rutas del proyecto
Las rutas a `datos/` y `assets/` se calculan usando `Path(__file__).resolve()`. Por ello, el funcionamiento no depende de la carpeta actual de la terminal y se evita el problema de rutas relativas al ejecutar el proyecto desde otra ubicación.

## Ejecución

1. Tener instalado Python 3 con Tkinter.
2. Abrir una terminal.
3. Entrar a la carpeta `restaurante_app`.
4. Ejecutar:

```bash
python main.py
```

También puede ejecutarse indicando directamente la ruta de `main.py`, porque los JSON y recursos visuales utilizan rutas basadas en la ubicación real de los archivos del proyecto.

## Credenciales de prueba

### Administrador
- Usuario: `admin`
- Contraseña: `1234`
- Rol: `Administrador`
- Tiene acceso a la gestión administrativa de usuarios.

### Cliente
- Usuario: `viviana`
- Contraseña: `2026`
- Rol: `Cliente`
- No dispone de la pestaña administrativa de usuarios.

### Empleado
- Usuario: `empleado`
- Contraseña: `5678`
- Rol: `Empleado`
- No dispone de la pestaña administrativa de usuarios.

## Comprobación funcional sugerida

1. Iniciar sesión como `admin`.
2. Abrir **Usuarios**.
3. Registrar un Cliente o Empleado y comprobar que aparece en el `Treeview`.
4. Seleccionar una fila y comprobar que los datos se cargan automáticamente.
5. Modificar un dato y pulsar **Actualizar**.
6. Seleccionar un usuario no administrador y pulsar **Eliminar**; confirmar la operación.
7. Presionar `Enter` desde el formulario para registrar un usuario.
8. Presionar `Esc` para limpiar el formulario y la selección.
9. Cambiar el rol en el `Combobox` y comprobar la respuesta visual.
10. Cerrar y abrir la aplicación para verificar que los cambios permanecen en `usuarios.json`.
11. Iniciar sesión como `viviana` o `empleado` y comprobar que no aparece la pestaña administrativa de Usuarios.
12. Verificar que Productos y Ventas continúan funcionando.

## Entrega
La entrega solicitada en Moodle corresponde únicamente al **enlace público del repositorio GitHub de la Semana 16**. Antes de enviar, se debe comprobar que el repositorio sea público, accesible y contenga todos los archivos mostrados en la estructura anterior.
