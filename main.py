import logging 

from abc import ABC, abstractmethod 

 

# Configuracion del archivo de registros 

logging.basicConfig( 

    filename="eventos.log", 

    level=logging.INFO, 

    format="%(asctime)s - %(levelname)s - %(message)s" 

) 

 

 

# EXCEPCIONES PERSONALIZADAS 

class ErrorCliente(Exception): 

    pass 

 

 

class ErrorServicio(Exception): 

    pass 

 

 

class ErrorReserva(Exception): 

    pass 

 

 

# CLASE ABSTRACTA 

class Entidad(ABC): 

 

    @abstractmethod 

    def mostrar_informacion(self): 

        pass 

 

 

# CLASE CLIENTE 

class Cliente(Entidad): 

 

    def __init__(self, nombre, documento, correo): 

        if not nombre.strip(): 

            raise ErrorCliente("El nombre no puede estar vacio.") 

        if not documento.strip(): 

            raise ErrorCliente("El documento es obligatorio.") 

        if "@" not in correo: 

            raise ErrorCliente("El correo no es valido.") 

 

        self.__nombre = nombre 

        self.__documento = documento 

        self.__correo = correo 

 

    @property 

    def documento(self): 

        return self.__documento 

 

    def mostrar_informacion(self): 

        return ( 

            f"Cliente: {self.__nombre} | " 

            f"Documento: {self.__documento} | " 

            f"Correo: {self.__correo}" 

        ) 

 

 

# CLASE ABSTRACTA SERVICIO 

class Servicio(ABC): 

 

    def __init__(self, nombre, precio): 

        if not nombre.strip() or precio <= 0: 

            raise ErrorServicio("Datos del servicio invalidos.") 

 

        self.nombre = nombre 

        self.precio = precio 

 

    @abstractmethod 

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0): 

        pass 

 

    def describir(self): 

        return self.nombre 

 

 

# SERVICIO DE SALAS 

class Sala(Servicio): 

 

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0): 

        total = self.precio * duracion 

        return total - descuento + impuesto 

 

 

# ALQUILER DE EQUIPOS 

class Equipo(Servicio): 

 

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0): 

        total = self.precio * duracion 

        return total - descuento + impuesto 

 

 

# ASESORIAS ESPECIALIZADAS 

class Asesoria(Servicio): 

 

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0): 

        total = self.precio * duracion 

        return total - descuento + impuesto 

 

 

# CLASE RESERVA 

class Reserva: 

 

    def __init__(self, cliente, servicio, duracion): 

        if duracion <= 0: 

            raise ErrorReserva("La duracion debe ser mayor que cero.") 

 

        self.cliente = cliente 

        self.servicio = servicio 

        self.duracion = duracion 

        self.estado = "Pendiente" 

 

    def confirmar(self): 

        if self.estado != "Pendiente": 

            raise ErrorReserva("La reserva no puede confirmarse.") 

        self.estado = "Confirmada" 

        logging.info("Reserva confirmada.") 

 

    def cancelar(self): 

        if self.estado == "Cancelada": 

            raise ErrorReserva("La reserva ya esta cancelada.") 

        self.estado = "Cancelada" 

        logging.info("Reserva cancelada.") 

 

    def procesar(self): 

        try: 

            if self.estado != "Confirmada": 

                raise ErrorReserva("La reserva no esta confirmada.") 

 

            total = self.servicio.calcular_costo(self.duracion) 

            logging.info("Reserva procesada correctamente.") 

            return total 

 

        except ErrorReserva as error: 

            logging.error(f"Error al procesar reserva: {error}") 

            raise ErrorReserva("No fue posible procesar la reserva.") from error 

 

        finally: 

            print("Finalizo el intento de procesamiento.") 

 

 

# SISTEMA INTEGRAL 

class SistemaGestion: 

 

    def __init__(self): 

        self.clientes = [] 

        self.servicios = [] 

        self.reservas = [] 

 

    def registrar_cliente(self, cliente): 

        if any(c.documento == cliente.documento for c in self.clientes): 

            raise ErrorCliente("El cliente ya esta registrado.") 

 

        self.clientes.append(cliente) 

        logging.info("Cliente registrado.") 

        print("Cliente registrado correctamente.") 

 

    def registrar_servicio(self, servicio): 

        self.servicios.append(servicio) 

        logging.info("Servicio registrado.") 

        print("Servicio registrado correctamente.") 

 

    def crear_reserva(self, cliente, servicio, duracion): 

        if cliente not in self.clientes: 

            raise ErrorReserva("El cliente no esta registrado.") 

 

        if servicio not in self.servicios: 

            raise ErrorReserva("El servicio no esta disponible.") 

 

        reserva = Reserva(cliente, servicio, duracion) 

        self.reservas.append(reserva) 

        logging.info("Reserva creada.") 

        print("Reserva creada correctamente.") 

        return reserva 

 

 

# PRUEBAS DEL SISTEMA 

def ejecutar_pruebas(): 

 

    sistema = SistemaGestion() 

 

    print("\nSISTEMA INTEGRAL DE GESTION") 

    print("EMPRESA SOFTWARE FJ\n") 

 

    # OPERACION 1: Registrar cliente 

    try: 

        cliente1 = Cliente( 

            "Laura Perez", "1001", "laura@gmail.com" 

        ) 

        sistema.registrar_cliente(cliente1) 

    except ErrorCliente as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 2: Registrar otro cliente 

    try: 

        cliente2 = Cliente( 

            "Carlos Gomez", "1002", "carlos@gmail.com" 

        ) 

        sistema.registrar_cliente(cliente2) 

    except ErrorCliente as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 3: Intentar registrar cliente invalido 

    try: 

        cliente_invalido = Cliente("", "1003", "correo") 

        sistema.registrar_cliente(cliente_invalido) 

    except ErrorCliente as error: 

        logging.error(str(error)) 

        print("Error controlado:", error) 

 

    # OPERACION 4: Crear servicio de sala 

    try: 

        sala = Sala("Reserva de sala", 50000) 

        sistema.registrar_servicio(sala) 

    except ErrorServicio as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 5: Crear servicio de equipo 

    try: 

        equipo = Equipo("Alquiler de computador", 30000) 

        sistema.registrar_servicio(equipo) 

    except ErrorServicio as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 6: Crear servicio de asesoria 

    try: 

        asesoria = Asesoria("Asesoria especializada", 80000) 

        sistema.registrar_servicio(asesoria) 

    except ErrorServicio as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 7: Intentar crear servicio invalido 

    try: 

        servicio_invalido = Sala("Sala", -100) 

        sistema.registrar_servicio(servicio_invalido) 

    except ErrorServicio as error: 

        logging.error(str(error)) 

        print("Error controlado:", error) 

 

    # OPERACION 8: Crear reserva 

    try: 

        reserva1 = sistema.crear_reserva(cliente1, sala, 2) 

    except ErrorReserva as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 9: Confirmar y procesar reserva 

    try: 

        reserva1.confirmar() 

        total = reserva1.procesar() 

        print("Costo de la reserva:", total) 

    except ErrorReserva as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 10: Crear y cancelar reserva 

    try: 

        reserva2 = sistema.crear_reserva(cliente2, equipo, 3) 

        reserva2.cancelar() 

        print("Estado:", reserva2.estado) 

    except ErrorReserva as error: 

        logging.error(str(error)) 

        print(error) 

 

    # OPERACION 11: Intentar procesar reserva cancelada 

    try: 

        reserva2.procesar() 

    except ErrorReserva as error: 

        logging.error(str(error)) 

        print("Error controlado:", error) 

 

    # OPERACION 12: Calculo con parametros adicionales 

    try: 

        costo = sala.calcular_costo(2, 5000, 2000) 

        print("Costo con descuento e impuesto:", costo) 

    except Exception as error: 

        logging.error(str(error)) 

        print(error) 

 

    # RESUMEN 

    print("\nRESUMEN DEL SISTEMA") 

    print("Clientes registrados:", len(sistema.clientes)) 

    print("Servicios registrados:", len(sistema.servicios)) 

    print("Reservas realizadas:", len(sistema.reservas)) 

    print("Las pruebas finalizaron correctamente.") 

    print("Consulte el archivo eventos.log para ver los registros.") 

 

 

if __name__ == "__main__": 

    ejecutar_pruebas() 
