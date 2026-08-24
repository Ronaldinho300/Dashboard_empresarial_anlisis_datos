import pandas as pd

from Dashboard_empresarial_anlisis_datos.estado import State


def test_ir_a_grafico_producto_mas_vendido():
    state = State()
    state._df = pd.DataFrame(
        {
            "producto": ["A", "B", "A"],
            "venta": [10, 5, 4],
            "sede": ["Lima", "Lima", "Cusco"],
            "categoria": ["Cat", "Cat", "Dog"],
            "fecha": ["2024-01-01", "2024-01-02", "2024-01-03"],
        }
    )
    state.producto_mas_vendido = "A"

    state.ir_a_grafico("producto")

    assert state.vista_activa == "graficos"
    assert state.eje_x == "producto"
    assert state.eje_y == "venta"
    assert state.tipo_grafico == "barras"
