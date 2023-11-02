from eddy_pdu import EddyEps

def eps_data_organization():
    eps = EddyEps(smbus_num=1)
    # eps.print_measurement_table()


    # print( ['V VBATT RAW', eps.get_voltage_vbatt_raw(), 'V'],
    #       ['I VBATT RAW', eps.get_current_vbatt_raw(), 'A'],
    #       ['V 3V3', eps.get_voltage_3v3(), 'V'],
    #       ['I 3V3', eps.get_current_3v3(), 'A'],
    #       ['V 5V0', eps.get_voltage_5v0(), 'V'],
    #       ['I 5V0', eps.get_current_5v0(), 'A'],
    #       ['V VBATT', eps.get_voltage_vbatt(), 'V'],
    #       ['I VBATT', eps.get_current_vbatt(), 'A'],
    #       ['3V3 REG TEMP', eps.get_temp_3v3_reg(), 'C'],
    #       ['3V3 REG TEMP', eps.get_temp_3v3_reg(unit='f'), 'F'],
    #       ['5V0 REG TEMP', eps.get_temp_5v0_reg(), 'C'],
    #       ['5V0 REG TEMP', eps.get_temp_5v0_reg(unit='f'), 'F'],
    #)

    vol_vbatt_raw = eps.get_voltage_vbatt_raw()
    curr_vbatt_raw = eps.get_current_vbatt_raw()
    vol_3v3 = eps.get_voltage_3v3()
    curr_3v3 = eps.get_current_3v3()
    vol_5v0 = eps.get_voltage_5v0()
    curr_5v0 = eps.get_current_5v0()
    volt_vbatt = eps.get_voltage_vbatt()
    curr_vbatt = eps.get_current_vbatt()
    reg_temp_3v3_C = eps.get_temp_3v3_reg()
    reg_temp_3v3_F = eps.get_temp_3v3_reg(unit='f')
    reg_temp_5v0_C = eps.get_temp_5v0_reg()
    reg_temp_5v0_F = eps.get_temp_5v0_reg(unit='f')

    eps_telem_list = [vol_vbatt_raw, curr_vbatt_raw, vol_3v3, curr_3v3, vol_5v0, curr_5v0, volt_vbatt, curr_vbatt, 
                    reg_temp_3v3_C, reg_temp_3v3_F, reg_temp_5v0_C, reg_temp_5v0_F]

    return eps_telem_list