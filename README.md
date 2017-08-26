### Application Server

Se trata de una aplicación por consola destinada a mantenerse en ejecución por perí­odos prolongados de tiempo.

Esta aplicación debe brindar una interfaz REST [1] para la comunicación de los diferentes clientes (choferes y pasajeros) que se conecten. El objetivo principal de cara a los choferes proveerles los posibles viajes a realizar, y de cara a los pasajeros mostrarles los posibles choferes para que realicen el viaje.

Este servidor se comunicará con el _Shared server_ (explicado a continuación) a traves de la interfaz REST común definida para el mismo. En el caso que la _aplicación Android_ (explicada a continuación) necesitará de algún servicio del _Shared Server_, el _Application server_ deberá de actuar de fachada.

#### Servicio de registro

Este servicio permitirá a los usuarios darse de alta en el sistema. Además, deberá almacenar la información del nuevo usuario en el _Shared server_.

#### Servicio de modificación de perfil

Este servicio permite a un usuario actualizar su perfil, debe permitir modificar y actualizar los siguientes datos:

* Datos personales (Nombre, Apellido, EMail, Cuenta de Facebook, GMail, etc)
* _(En caso de ser chofer)_ Datos acerca del auto (Modelo, Color, patente, año, estado, aire acondicionado, radio o música que se escucha)
* _(En caso de ser pasajero)_ Datos de cobranza

#### Servicio de direccionamiento

Servicio que utilizará a uno de un tercero para poder determinar los caminos posibles para el viaje que quiera hacer el pasajero. Se deberá utilizar algún servicio de direccionamiento como lo puede ser [Google Directions Api](https://developers.google.com/maps/documentation/directions/).

#### Servicio de viajes disponibles

Este servicio permite a un chofer saber que viajes tiene disponibles para aceptar. Debe brindar al chofer toda la  información acerca del pasajero y el viaje. Además, debe proporcionar la sugerencia del viaje aceptada por el pasajero.

#### Servicio de choferes disponibles

Este servicio permite a los pasajeros visualizar los choferes que se encuentran a su alrededor. Debe dar la posición del chofer, además, de información acerca de í©l.

#### Servicio de posicionamiento

Una vez iniciado un viaje, el servidor deberá poseer la posición tanto del conductor y pasajero. Para ello, ambos enviarán periódicamente su posición. Esto permitirá al servidor:

* Corroborar que realmente se está realizando el viaje.
* Calcular la distancia y tiempo de viaje con exactitud

#### Servicio de cotización de viaje

Permite saber, con un margen de error, el costo de un viaje antes de realizarlo. Este servicio será una fachada de uno proporcionado por el Shared Server.
