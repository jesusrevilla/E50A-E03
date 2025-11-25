# E50A-E03
Examen del tercer parcial

## 1. Joins y Vistas

Imagina que tienes las siguientes tablas llamada `clientes`, `productos` , `pedidos` y `detalle_pedido`:

```sql

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100)
);

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10, 2)
);

CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha DATE
);

CREATE TABLE detalle_pedido (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT
);
```

```sql
-- Clientes
INSERT INTO clientes (nombre, correo) VALUES
('Ana Torres', 'ana@example.com'),
('Luis Pérez', 'luis@example.com');

-- Productos
INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200.00),
('Mouse', 25.50),
('Teclado', 45.00);

-- Pedidos
INSERT INTO pedidos (id_cliente, fecha) VALUES
(1, '2025-05-01'),
(2, '2025-05-02');

-- Detalle de pedidos
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES
(1, 1, 1),  -- Ana compra 1 Laptop
(1, 2, 2),  -- Ana compra 2 Mouse
(2, 3, 1);  -- Luis compra 1 Teclado
```

👁️ Crear una vista con JOINs (vista_detalle_pedidos)
Esta vista muestra el detalle de cada pedido, incluyendo el nombre del cliente, producto, cantidad y el total por línea.


🔍 Consultar la vista
```sql
SELECT * FROM vista_detalle_pedidos;
```


## 2. Procedimiento almacenado

🛠️  Registrar un nuevo pedido
Este procedimiento llamado registrar_pedido inserta un nuevo pedido y sus detalles en varias tablas. 

Ejemplo de uso:
```sql
CALL registrar_pedido(1, '2025-05-20', 2, 3);
```

## 3. Función

🧮 Calcula el total gastado por un cliente
Esta función devuelve el total gastado por un cliente sumando todos sus pedidos.

Ejemplo de uso

```sql
SELECT total_gastado_por_cliente(1);
```

Y crea un índice compuesto llamado idx_cliente_producto

## 4. Disparadores (Triggers)

Crear un trigger que registre en una tabla de auditoría cada vez   
que se inserte un nuevo pedido, incluyendo el ID del cliente,   
la fecha del pedido y la fecha y hora del registro.  

🧱 Crear las tablas necesarias
```sql
-- Tabla de auditoría
CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

⚙️ Crear la función que será llamada por el trigger

🔔 3. Crear el trigger   



✅ 4. Probar el trigger
```sql
-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

```


## 5. NoSQL

Bases de Datos NoSQL (usando JSON en PostgreSQL)
Aunque PostgreSQL es una base de datos relacional,   
permite trabajar con estructuras NoSQL usando   
tipos de datos como JSON y JSONB.

🎯 Objetivo
Guardar información flexible de productos con atributos variables usando JSONB.

🧱 Crear tabla con campo JSONB

```sql
CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

```

📥 Insertar datos con estructura flexible

```sql
INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Smartphone', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad Air", "color": "gris"}');
```

🔍 Consultar productos con un atributo específico
```sql
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';
``` 

Registro de usuarios con historial de actividad (JSONB)    

🎯 Objetivo   
Modelar una tabla de usuarios donde cada usuario tiene   
un historial de actividades almacenado como un arreglo de objetos JSON.   

🧱 Crear la tabla

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);
```
📥 Insertar datos con historial de actividad

```sql
INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez', 'laura@example.com', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-02", "accion": "subio_archivo"},
    {"fecha": "2025-05-03", "accion": "cerró_sesion"}
]'),
('Pedro Ruiz', 'pedro@example.com', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-04", "accion": "comentó_publicación"}
]');
```

🔍 Consultar usuarios que realizaron una acción específica

```sql
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
```
🔍 Extraer todas las acciones de un usuario



## 6. Gráfos

🕸️ Red de conexiones entre ciudades   

🎯 Objetivo
Modelar un grafo dirigido donde los nodos son ciudades   
y las aristas son rutas entre ellas con una distancia.   
Luego, realizar consultas para explorar las conexiones.

🧱 1. Crear las tablas

```sql
-- Nodos: ciudades
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Aristas: rutas entre ciudades
CREATE TABLE rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);
``` 
📥 2. Insertar datos

```sql
-- Ciudades
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

-- Rutas (grafo dirigido)
INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),  -- SLP → Querétaro
(2, 3, 350),  -- Querétaro → Guadalajara
(1, 5, 410),  -- SLP → CDMX
(5, 4, 900),  -- CDMX → Monterrey
(3, 4, 700);  -- Guadalajara → Monterrey

``` 
🔍 3. Consulta útil   
Ver todas las rutas desde San Luis Potosí   
