from easysnmp import snmp_get

def get_data_by_snmp():
    data = snmp_get('1.3.6.1.4.1.40418.2.2.4.2', hostname='192.168.15.20', community='public', version=1)
    return str(data).split("'")[1]