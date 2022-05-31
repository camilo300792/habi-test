# Habi test
## Stack usado

Para desarrollar esta prueba utilizamos docker como entorno para construir nuestra aplicación, también la libreria FastAPI para la creación del servicio rest requerido.
En cuanto a la elección de las herramientas de desarrollo podemos decir que docker nos permite un despliegue mucho más fácil quitandonos los tipicos problemas del desarrollo de software y FastAPI es una librería ligera con un performance muy bueno que facilita la construcción de API REST con los mejores estandares y nos permite autodocumenta la misma.

## Planificación y construcción del proyecto

Este proyecto lo abordé conociendo de primera mano el modelo de la BD el cuál analice y probe para construir los queries necesarios para la solución. Posteriormente construí tres archivos base que se encargan cada uno de una taarea especifica, uno se conecta a la BD, el otro sirve como repositorio de consultas y por ultimo el encargado de definir el endpoint y sus parametros; Respecto a este ultimo, los parametros se definen en la url como query params por lo que no encuentro necesario la construcción de un JSON especificandolos.

## Modelo relacional

Para el modelo relacional inicial propongo una mejora y es separar de la tabla property el campo city de forma tal que se convierta en una nueva tabla realcionada para normalizar los datos en la tabla property.
Para el segundo punto el servicio **Me gusta** propuce una unica tabla relacionada con property y con auth_user que cuenta con una bandera de *me gusta* para que se pueda intercambiar entre me gusta y no me gusta. la tabla almacena el historico de usuario, propiedad y fecha.

![Habi DB](https://github.com/camilo300792/habi-test/blob/main/habi_db.png)

## Propuesta de mejora

```mysql
INSERT INTO cities (name)
SELECT DISTINCT city from property p 
WHERE city IS NOT NULL 
AND city NOT IN ('')

ALTER TABLE property
ADD COLUMN city_id INT;

ALTER TABLE property
ADD CONSTRAINT FK_property_city
FOREIGN KEY (city_id) REFERENCES cities(id);

UPDATE property
LEFT JOIN cities ON property.name = cities.city
SET cities.city_id = (
	CASE 
		WHEN property.city = '' OR property.city IS NULL THEN 1 
	ELSE cities.id 
)

ALTER TABLE property
DROP COLUMN city;
```

## Extendiendo el modelo *servicio me gusta* 

```mysql
CREATE TABLE cities (
	user_id INT NOT NULL,
  	property_id INT NOT NULL,
  	i_like TINYINT NOT NULL DEFAULT 1,
  	created_at DATETIME NOT NULL
  	UNIQUE INDEX `uq_user_property` (`user_id` ASC, `property_id` ASC) INVISIBLE
);


ALTER TABLE i_like_history
ADD CONSTRAINT fk_i_like_history_property
FOREIGN KEY (property_id) REFERENCES property(id);

ALTER TABLE i_like_history
ADD CONSTRAINT fk_i_like_history_auth_user
FOREIGN KEY (user_id) REFERENCES auth_user(id);
```
