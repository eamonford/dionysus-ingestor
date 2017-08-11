from DataAccessor import DataAccessor

class SensorDataAccessor(DataAccessor):

    def __init__(self, connection):
        super(SensorDataAccessor, self).__init__("sensors", connection)

    def getByDeviceId(self, device_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM " + self.table + " WHERE device_id = '" + device_id + "'")
        except:
            raise
        else:
            return self._makeDictOfResponse(cursor.description,
                                             cursor.fetchall())
        finally:
            cursor.close()
