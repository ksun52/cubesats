
import bme680
import time

sensor = bme680.BME680(0x77)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


def get_bme_dict(data_dict):
    BME = bme680.BME680()
    BME.get_sensor_data()

    data_dict["BMETemp"] = BME.data.temperature # celcius
    data_dict["BMEPressure"] = BME.data.pressure # mbar
    data_dict["BMEHumidity"] = BME.data.humidity # relative hum.
