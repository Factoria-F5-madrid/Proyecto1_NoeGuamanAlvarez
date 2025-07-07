import pytest
import time
from taximetro2 import Taximetro


@pytest.fixture
def taximetro():
    return Taximetro()


def test_iniciar_viaje_activa_viaje(taximetro):
    taximetro.iniciar_viaje()
    assert taximetro.viaje_activo is True
    assert taximetro.estado_viaje == "parado"
    assert isinstance(taximetro.tiempo_inicio, float)


def test_iniciar_viaje_dos_veces_muestra_error(capfd, taximetro):
    """
    capfd es un fixture especial de pytest que captura la salida de consola
    (tanto lo que se imprime con print() como los errores estándar).
    Sirve para verificar que tu función realmente imprimió lo que esperabas.
    """
    taximetro.iniciar_viaje()
    taximetro.iniciar_viaje()
    out, _ = capfd.readouterr()
    """está dentro de"""
    assert "Error" in out


def test_cambiar_estado_actualiza_estado(taximetro):
    taximetro.iniciar_viaje()
    taximetro.cambiar_estado("moviendose")
    assert taximetro.estado_viaje == "moviendose"


def test_cambiar_estado_sin_iniciar(capfd, taximetro):
    taximetro.cambiar_estado("parado")
    out, _ = capfd.readouterr()
    assert "Error" in out


def test_actualizar_duracion_parado(taximetro):
    taximetro.iniciar_viaje()
    time.sleep(1)
    taximetro._actualizar_duracion()
    assert taximetro.tiempo_parado >= 1.0


def test_configurar_precios_dinamicos(taximetro):
    taximetro.configurar_precios_dinamicos(0.5, 1.2)
    assert taximetro.precio_parado_dinamico == 0.5
    assert taximetro.precio_movimiento_dinamico == 1.2


def test_finalizar_viaje_con_precios_dinamicos(caplog, taximetro):
    """caplog es un fixture incorporado en pytest que te permite capturar los mensajes de log
    (logging.info, logging.warning, etc.) generados por tu código durante una prueba."""
    caplog.set_level("INFO")
    taximetro.configurar_precios_dinamicos(0.1, 0.2)
    taximetro.iniciar_viaje()
    time.sleep(1)
    taximetro.cambiar_estado("moviendose")
    time.sleep(1)
    taximetro.finalizar_viaje(2)
    """Accedemos a ellos con caplog.text"""
    assert any("Viaje finalizado" in record.message for record in caplog.records)


def test_finalizar_sin_iniciar(capfd, taximetro):
    taximetro.finalizar_viaje(opcion_precio=1)
    out, _ = capfd.readouterr()
    assert "Error, el viaje no ha iniciado" in out
