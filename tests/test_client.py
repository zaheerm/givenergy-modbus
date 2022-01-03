from unittest.mock import MagicMock as Mock

import pytest

from givenergy_modbus.client import GivEnergyModbusClient
from givenergy_modbus.model.register_banks import HoldingRegister
from givenergy_modbus.pdu import ReadHoldingRegistersRequest, ReadInputRegistersRequest


def test_read_all_holding_registers():
    """Ensure we read the ranges of known registers."""
    c = GivEnergyModbusClient()
    mock_call = Mock(name='execute', return_value=Mock(register_values=[1, 2, 3], name='ReadHoldingRegistersResponse'))
    c.execute = mock_call
    assert c.read_all_holding_registers() == [1, 2, 3, 1, 2, 3, 1, 2, 3]
    assert mock_call.call_count == 3
    req1 = mock_call.call_args_list[0].args[0]
    req2 = mock_call.call_args_list[1].args[0]
    req3 = mock_call.call_args_list[2].args[0]

    assert req1.__class__ == ReadHoldingRegistersRequest
    assert req1.base_register == 0
    assert req1.register_count == 60
    assert req2.__class__ == ReadHoldingRegistersRequest
    assert req2.base_register == 60
    assert req2.register_count == 60
    assert req3.__class__ == ReadHoldingRegistersRequest
    assert req3.base_register == 120
    assert req3.register_count == 1


def test_read_all_input_registers():
    """Ensure we read the ranges of known registers."""
    c = GivEnergyModbusClient()
    mock_call = Mock(name='execute', return_value=Mock(register_values=[1, 2, 3], name='ReadInputRegistersResponse'))
    c.execute = mock_call
    assert c.read_all_input_registers() == [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    assert mock_call.call_count == 4
    req1 = mock_call.call_args_list[0].args[0]
    req2 = mock_call.call_args_list[1].args[0]
    req3 = mock_call.call_args_list[2].args[0]
    req4 = mock_call.call_args_list[3].args[0]

    assert req1.__class__ == ReadInputRegistersRequest
    assert req1.base_register == 0
    assert req1.register_count == 60
    assert req2.__class__ == ReadInputRegistersRequest
    assert req2.base_register == 60
    assert req2.register_count == 60
    assert req3.__class__ == ReadInputRegistersRequest
    assert req3.base_register == 120
    assert req3.register_count == 60
    assert req4.__class__ == ReadInputRegistersRequest
    assert req4.base_register == 180
    assert req4.register_count == 2


def test_write_holding_register():
    """Ensure we can write to holding registers."""
    c = GivEnergyModbusClient()
    mock_call = Mock(name='execute', return_value=Mock(value=5, name='WriteHoldingRegisterResponse'))
    c.execute = mock_call
    c.write_holding_register(HoldingRegister.WINTER_MODE, 5)
    assert mock_call.call_count == 1

    mock_call = Mock(name='execute', return_value=Mock(value=2, name='WriteHoldingRegisterResponse'))
    c.execute = mock_call
    with pytest.raises(ValueError) as e:
        c.write_holding_register(HoldingRegister.WINTER_MODE, 5)
    assert mock_call.call_count == 1
    assert e.value.args[0] == 'Returned value 2 != written value 5.'

    mock_call = Mock(name='execute', return_value=Mock(value=2, name='WriteHoldingRegisterResponse'))
    with pytest.raises(ValueError) as e:
        c.write_holding_register(HoldingRegister.INVERTER_STATE, 5)
    assert mock_call.call_count == 0
    assert e.value.args[0] == 'Register INVERTER_STATE is not safe to write to.'
