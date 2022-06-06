from .dbclient import DBClient


class HabiRepository:

    __connection = None
    
    @classmethod
    def getProperty(cls, build_year = None, city = None, status = None):
        query_property = (
            "SELECT DISTINCT "
            "p.id "
            ", p.address "
            ", p.city "
            ", s.name "
            ", p.price "
            ", p.description "
            "FROM status_history sh "
            "INNER JOIN ("
            "    SELECT DISTINCT "
            "        sh.property_id, "
            "        MAX(sh.update_date) max_date "
            "    FROM status_history sh "
            "    GROUP BY sh.property_id "
            ") aux ON sh.property_id = aux.property_id AND sh.update_date = max_date "
            "INNER JOIN property p ON sh.property_id = p.id "
            "INNER JOIN status s ON sh.status_id = s.id "
            "WHERE s.id IN (3, 4, 5) "
        )
        data = []
        if build_year is not None:
            query_property += "AND p.`year` = %s "
            data.append(build_year)
        if city is not None:
            query_property += "AND p.city = %s "
            data.append(city)
        if status is not None:
            query_property += "AND s.name = %s "
            data.append(status)        
        query_property += "GROUP BY p.address, p.city, p.price, p.description "
        query_property += "ORDER BY sh.id, sh.update_date DESC"
        params = tuple(data)
        cls.connect()
        cursor = cls.__connection.cursor()
        cursor.execute(query_property, params)
        result = []
        for (id, address, city, name, price, description) in cursor:
            result.append({
                'address': address,
                'city': city,
                'status': name,
                'price': price,
                'description': description
            })
            
        
        cursor.close()

        return result

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            cls.__connection = DBClient.connect()

    @classmethod
    def close(cls):
        cls.__connection.close()
        cls.__connection = None