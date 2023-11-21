"""
Python file used to edit the data in the database
"""
# Import necessary libraries
import csv
import pymysql.connector

# Create connection with master username and password, as well as create the cursor to execute commands
mydb = mysql.connector.connect(
    host="34.130.173.160",
    user="root",
    password="groupproject",
    database="music_schema"
)
mycursor = mydb.cursor(buffered=True)


def add_primary_key(table_name, attributes):
    """
    Adds a primary key to a table
    :param table_name: Name of the table being altered
    :param attributes: Attributes that will be part of the primary key
    """
    mycursor.execute(f'ALTER TABLE {table_name} DROP PRIMARY KEY;')
    mydb.commit()
    mycursor.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY ({", ".join(attributes)});')
    mydb.commit()


def modify_attribute(table_name, attribute, type, not_null):
    """
    Alters an attribute in a table through modification
    :param table_name: Name of the table where the attribute is located
    :param attribute: Name of the attribute being modified
    :param type: The attribute type, i.e. TEXT, CHAR, INT, etc.
    :param not_null: Boolean value of whether the attribute can contain NULL values or not
    """
    if not_null:
        mycursor.execute(f'ALTER TABLE {table_name} MODIFY {attribute} {type} NOT NULL;')
    else:
        mycursor.execute(f'ALTER TABLE {table_name} MODIFY {attribute} {type} NULL;')
    mydb.commit()


def create_constraint(table_name, constraint_name, predicate):
    """
    Adds a constraint to a table to uphold business logic or values
    :param table_name: Name of the table where the check is being made
    :param constraint_name: Unique name of the constraint
    :param predicate: Predicate value that defines the functionality of the constraint
    """
    mycursor.execute(f'ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name};')
    mydb.commit()
    mycursor.execute(f'ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} CHECK ( {predicate} );')
    mydb.commit()


def add_foreign_key(main_table, reference_table, attribute):
    """
    Adds a foreign key to create a relationship between two tables
    :param main_table: The table that contains the foreign key
    :param reference_table: The table being referenced by the foreign key
    :param attribute: Attribute being used as the key, usually the primary key in reference_table
    """
    mycursor.execute(
        f'ALTER TABLE {main_table} DROP FOREIGN KEY {main_table + "_" + reference_table + "_" + attribute}_fk;')
    mydb.commit()
    mycursor.execute(
        f'ALTER TABLE {main_table} ADD CONSTRAINT {main_table + "_" + reference_table + "_" + attribute}_fk FOREIGN KEY ({attribute}) REFERENCES {reference_table} ({attribute});')
    mydb.commit()


def insert_missed_records(missed_set, file_name, table_name, table_attributes):
    """
    Used to insert missing records that got missed when importing the data to the database
    :param missed_set: List of Primary Keys from the table that were missed
    :param file_name: File location of the original CSV file
    :param table_name: Name of the table that is being inserted into
    :param table_attributes: All attributes of the table
    """
    with open(file_name, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Base SQL statement that will insert one row, just requires values which are calculated in the for loop
        sql = f'INSERT INTO music_schema.{table_name} ({", ".join(table_attributes)}) VALUES (%s{", %s" * (len(table_attributes) - 1)})'
        for row in reader:
            # If the row in the CSV file are part of the missing set, it adds the attributes to the val list, and executes the SQL command
            if row[table_attributes[0]] in missed_set:
                val = []
                for attribute in table_attributes:
                    val.append(row[attribute])
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")


# Run the script.
if __name__ == '__main__':
    insert_missed_records(('0DDoHNUkFFMrFsTiqYYw45', '0kg0dT1yOc4475paTD0zfR', '6eilhBX00dAFSO11AUEIYh',
                           '0HwAncTXirU7D3I0JR30oe', '2g8PQWUjo6Qshdl5facuwK', '3v59w9liPFmENSJWJQP3eJ',
                           '5ukepQJXJryBcV5yXLE3rr', '5Veo9Cn6gUEM4SxzJ1Sanu', '3RxGY0Ja10d3BsHGvInk0d',
                           '0Q796V9ct16Mz6SSxRunHy', '4A9acD4a1H7paf22y2VFlq', '6txk1LEWt6iN8e83zbK3qG',
                           '4HWsgkVn90cVXh2JGJ1HEz', '4DHkzbZSWxsCsvRoEzr28A', '1WBGMBl9hFoa33PJGYcCwY',
                           '2p4WnpR3H16ywshkL2Fp1n', '3R6sUAasHimDVSNVQEG3md', '5cltWPM1GjCEShVZiz4cD3',
                           '23cS2EeU9dQS6jbcedtDer', '3WQfzH8NlFk9jltDK1Ei1p', '5mTw7pO7bUbCN9wdmKcCPw',
                           '61asDMua0oGUCDXOhIsN0u', '3o5szb3wXmja297QAuxy7V', '69kh0Ixnd3SvWdWKeuRxqt',
                           '5ti7VaeB65AHJUtnC2QNTb', '0G6RViEloMHJceb8orTNLi', '070veM2qP4jj3JXJBgnEHe',
                           '2hatTiwjfBt1mJtU4U7wtC', '2XaguXBOI15u8RbzpmDIu9', '0QmHXLu1AlAWvafXYu5tYf',
                           '4OYMgS2LefMWbPXIcTeLpU', '7bUhyQ8SuqQPxuzkbIMvVU', '2l6DzCeL9KWKUY7qYd51Zr',
                           '3OVzM5q8WGjtGPvbGmLeQP', '6deKWsZTjoa7WxOp8ML5Ni', '0PgekT75NSswPHGl2qLbsd',
                           '36ZPg3jJhjOkM8eH8bYLCS', '3qyrli8VQXdw9TiZqpqIfs', '66YhnYG6MgXFigmsy0fZEF',
                           '6aZv7TQ8LMKEkL7y22LdYt', '3hovkLdIHz3Ei7glaIUTDf', '6RGXwwuuXMQuEmhgTZGGDi',
                           '3t6X20cz3Rnul8axbAMdL6', '3zmNQU7SxSYEquKvGqTQDf', '3Ufm1A3655S5A8XunPIBpx',
                           '4jhOmwnOZQSxdHZ9ywdtCC', '6I5SbGFkdSKRegszp3sG2Y', '1dzrmxdYTY5YwgHs0SbNTN',
                           '69T698vkAQlSwnjtqwxFMf', '6GAYVXsTcrYaL9J224cYWi', '29uxMeKFYtZA4GYKBJ6QZS',
                           '3RpfO7oObzInjt62YKnZA3', '5op3JRnvhXC9UWfdvAa7oR', '7wseMOxZh4kygRYxwrj2K6',
                           '1q0Gtm6OaJHOvhLBRk3xYZ', '3XAFrqx6TjQCRRsMcfKPPe', '4XWLwl4V9idgddMQmcyP5X',
                           '5B0MjCXxBjXNl59S3VJuMR', '07oODhPq8CONzeliAIBZAU', '6Oi2dpSnnNPVDK8zXgTQL5',
                           '4gzpfALedoN5L0o15kJGWZ', '57atmZkje31ZaR7R0y1XD1', '1ljjGe2yv9wG0BAkHFqeHc',
                           '3VnEsEB2o8I0wdobKChJd0', '5niFswHK846w8bGZrOgHXe', '5fVyNTTpLwAeNGkx2FSJDt',
                           '6UX74txi5ckupCoiA4uo5Q', '0AnJGlNdR56Hco4c2f4IYz', '0nejfXN5tjdICWIdfakXWx',
                           '18cCBvygH6yEFDY0cYN3wT', '1JY6B9ILvmRla2IKKRZvnH', '1LikBIcmCec6zE64SHFcMK',
                           '1p2t6x0xFXuB6zWcZZ0SmZ', '2JgbGCxtzRp6wL5H1DgxV7', '2lNFWUrxuNaQsf5I1pDTPr',
                           '6BivCuyKJtgLa9ooFsvUoZ', '786ymAh5BmHoIpvjyrvjXk', '46ElgVtAOCnJYUz0z6qdW6',
                           '1n6h324Zk1HtWHHvD5r24x', '0uI60gwZupBx8dI4GYIYoK', '0uVppmRsJwcJ9bKHT4W6u8',
                           '535SNXRZZNrIABeLzMXgGr', '5C2UI3HkBUVcJqQeOXtSdA', '6juy4xM00OjwU8FVnklNH5',
                           '7N2klqE4VznUzC3jGKqeO4', '0TWcHrIxZ4TxlmnBMhIwGt', '3U31IUjHfwL1oNQaD7wyVv',
                           '4Tl0YJbMgJQfNHdJPc6I3G', '0tLitPsfIuc0igdAzZXz2L', '3x3coYHFPFBV7aOSeLbvwC',
                           '2w6NwhmKOSPoW7eEkidWWD', '4jRQYL5h4CDtbgdl6Mst1i', '4K5uNwnwPrtDhZOAhwuSoN',
                           '5iYFPjYLYDD10W0nNu8Rbi', '7n0pByoFvY1rjkfh6e8cu1', '7td7Wx6iNsQMak3iL0bzFq',
                           '0I1pVkh7UmCS9HoZ7jsjUb', '53kQoTWDqGnYXoog2asnuZ', '4ojdzH3gasxi7uWXyuZNHt',
                           '5NlQs9PwsUotsqUQ5NZP3w', '5TzyGPoiQASECRqu123V3d', '0htVQpnISTSokn6wXwtYmD',
                           '0LQAUpJU7GlphTHyE4s8sn', '4Htw9a6zKaU7Md0068M1ny', '4RH3uP7AmixpCWa4tUOu86',
                           '4uwMB1pTvX192ABzraVrex', '4x60DPdPLaY3faKsCRK5eb', '6IAY4TcBj71c1pHXl3vrEw',
                           '6iFd4PS1orZsFxFwHJzrn7', '5MtyZeQjxkkw4renCNRF3n', '2OkNDl4m0SyyqM0bxrrQUD',
                           '2SiONUuA1JLcJAHuUHkDDU', '0P75Zxe6ChU259t3Nv4nYK', '1VPSIhsmq55VXeobZK2qhF',
                           '1hznaPGDqmiOsUDmDo7nCx', '2V4VxRdbQpCxYDAUPxxiEB', '7oxl8YNgLaygBvXL9w9Vzs',
                           '2BJDApkbHwGrMd5ZhJLUAr', '6fA9GQ89dyaQBSyVdM7jzO', '4uuJFWo3S7DnwZ1XZO65TW',
                           '4fkV1Ksv1lZevspHkmspA8', '3ynkE6bonKI9CxQM3TtiIx', '0bou4k14OfCRus08rxN663',
                           '4txC6n35qJkJpQyocYtdlK', '43d5koQfZdpWXvGZeVpWqf', '1RY1QHOAvZ1a6JMpkVPDnc',
                           '2nLHtNoWCZVWzsAphyVkmK', '6O4uQLnD8TPaR446288Q5S', '78V1euRfiQkmWhbvCYmOBc',
                           '3MJufChxzPAFWrlCzauC5A', '1v9IihBzrudpxeTlO6Y1On', '3HsliYsDG1d9TLYEtwvWRj',
                           '1AMmRASh5oSubqWWvUavGC', '3qeOvNZjYc9vOgOgtDn0c2', '11WzU6XIfSTTKLz5oHeEyf',
                           '1GhfISdEzMeXFVYsPrI7wZ', '48vInJfRkJ0DI1iKD2Doip', '5hKXGqEj8YgzwZ1hYEChvs',
                           '5lsyTI8iYqHic2js4x2Vsp', '64qD9DZbJnN3zzbuu4da39', '6LBJnjyUi86j2RKwsSFniS',
                           '7EMgrsrbdDOT9YuKWf0keP', '3kjx9S2udBNRGoVEyzxID7', '7zXgEr6mv3z3gdtQvIL9NA',
                           '0DO3Lo7p5pH1W7xLrLwXvU', '1lq0ZSSaeyHYC3BwOX4g8g', '1wpuUxe790DB3g9oJTSYla',
                           '2478R7KuMFOkvkvp3fPLe9', '3i5rrfA2oN6N57jzeVPE0s', '3GqxlYfRz3EX2I3Go3mKZ0',
                           '0IGsM8dVAg0d70aYbmZgpN', '7eB0XYsREaG0TpxDXmCWmS', '64JghUayIoHpzNq16oVzgg',
                           '2rZxLWJYcUXsfgPtap7bjk', '06RrgrRd9W2OM4Mc2xyrX6', '15QLspFfy3qz2nmXLz8jgI',
                           '0MC4w7PegyVJ1VqCEN9Gdc', '3hEzFKjw98gL2NhgJbDlvK', '4beMM2PXK7gWj7siLsIJc6',
                           '7ebHAZ6dLZw9wS1Bf7qPI8', '7pdOoF2lmx5fRN3LXxfOiT', '6UmWNMFByqOoycPRJxblxr',
                           '5ortulXKnjCkK2NG7keX92', '7KPe6pLwX4Kc34RBhxiBnE', '4J0da2kgtlYmjgklB4bc4J',
                           '124b1kn2PqnyJ0NIpxCjKp', '1REKZGbvfUlA618peRhADw', '4EwPSrlazzLG9Olz5RVjC4',
                           '6qkArjoKS0Dt4rzLuxaAXE', '6E9qiMHjWZph2u7Aw8QG8z', '6aJlVCHtNB3bEkmGeDzrsX',
                           '1X9kWXmkga3jr3w7YTOjdt', '50K82MlUE2eC83Pqhkkft7', '1iHLgWF5sInxfWYEfU8Cht',
                           '4SSeQ74txpRULzJr1fXrVp', '0lwqWJeViDGF2ghQLFJi7D'),
                          'C:\\Users\\kobeo\\Documents\\School\\CSCI 620\\music\\sp_track.csv',
                          'sp_track',
                          ('track_id', 'track_title', 'duration_ms', 'isrc', 'track_number', 'release_id', 'explicit',
                           'disc_number', 'preview_url', 'updated_on'))
