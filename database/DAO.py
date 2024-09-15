from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(datetime) as year
                        from sighting s
                        order by year"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape
                            from sighting s
                            where year(datetime) = %s
                            order by shape"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                    from sighting s
                    where year(datetime) = %s and shape = %s"""
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(year, shape):
        """
        ritorna una tupla id1, id2, weight
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2, abs(s1.longitude - s2.longitude) as weight
                    from sighting s1, sighting s2
                    where s1.state = s2.state and s1.longitude < s2.longitude
                    and year(s1.datetime) = %s and year(s2.datetime) = year(s1.datetime)
                    and s1.shape = %s and s2.shape = s1.shape"""
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append((row["id1"], row["id2"], row["weight"]))
            cursor.close()
            cnx.close()
        return result
