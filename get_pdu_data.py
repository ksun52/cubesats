from eddy_pdu import EddyEps

eps = EddyEps(smbus_num=1)
eps.print_measurement_table()


print( ['V VBATT RAW', eps.get_voltage_vbatt_raw(), 'V'],
       ['I VBATT RAW', eps.get_current_vbatt_raw(), 'A'],
       ['V 3V3', eps.get_voltage_3v3(), 'V'],
       ['I 3V3', eps.get_current_3v3(), 'A'],
       ['V 5V0', eps.get_voltage_5v0(), 'V'],
       ['I 5V0', eps.get_current_5v0(), 'A'],
       ['V VBATT', eps.get_voltage_vbatt(), 'V'],
       ['I VBATT', eps.get_current_vbatt(), 'A'],
       ['3V3 REG TEMP', eps.get_temp_3v3_reg(), 'C'],
       ['3V3 REG TEMP', eps.get_temp_3v3_reg(unit='f'), 'F'],
       ['5V0 REG TEMP', eps.get_temp_5v0_reg(), 'C'],
       ['5V0 REG TEMP', eps.get_temp_5v0_reg(unit='f'), 'F'],
)