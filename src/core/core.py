import psycopg2
from psycopg2 import Error


class Postgresdb:
    def __init__(self, db_url=None, db_name=None, db_user=None, db_password=None, db_host=None, db_port=None, ssl=None):
        try:
            if db_url is not None:
                self.connection = psycopg2.connect(db_url, sslmode='require')

            else:
                self.connection = psycopg2.connect(
                    database=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port,
                )
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print('Error occured when connectng to database:', error)

    def delete_user(self, tablename, attribute, value):
        if isinstance(value, str) == True:
            value = "'" + value + "'"
        try:
            print(f'Deleting user {value} from table {tablename} . . .')
            query = f'''DELETE FROM {tablename} WHERE {attribute} = {value}'''
            self.cursor.execute(query)
            self.connection.commit()
            print(f'Successfully deleted user {value} from {tablename}')
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

    def add_user(self, tablename, fields, values):
        for element in fields:
            if isinstance(element, str) == True:
                element = "'" + element + "'"
        for element in values:
            if isinstance(element, str) == True:
                element = "'" + element + "'"

        if len(fields) > 1:
            fields = ', '.join(fields)
        fields = "(" + fields + ")"
        if len(values) > 1:
            values = ', '.join(values)
        values = "(" + values + ")"
        try:
            print(f'Inserting user {values} into table {tablename} . . .')
            query = f'''INSERT INTO {tablename} {fields} VALUES {values}'''
            self.cursor.execute(query)
            self.connection.commit()
            print(f'Successfully inserted {values} into {tablename}')
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

    def get_all_users(self, tablename):
        try:
            print(f'Getting all entries from {tablename} . . .')
            query = f'''SELECT * from {tablename}'''
            self.cursor.execute(query)
            entries = [user for user in self.cursor.fetchall()]
            print(f'All entires from {tablename}:', entries, '\n')
            return entries
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

    def create_table(self, tablename, fields):
        try:
            print(f'Creating table {tablename} . . .')
            query = f'''CREATE TABLE {tablename}
                    {fields}; '''
            self.cursor.execute(query)
            self.connection.commit()
            print(f'Successfully created {tablename}\n')
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

    def delete_table(self, tablename):
        try:
            print(f'Deleting table {tablename} . . .')
            query = f'''DROP TABLE {tablename}'''
            self.cursor.execute(query)
            self.connection.commit()
            print(f'Successfully deleted {tablename}\n')
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

    def update_fields(self, tablename, target_fields, target_values, new_values):
        for element in target_values:
            if isinstance(element, str) == True:
                element = "'" + element + "'"
        for element in new_values:
            if isinstance(element, str) == True:
                element = "'" + element + "'"

        target_records = []
        for i in range(len(target_fields)):
            target_records.append(str(target_fields[i]) + ' = ' + str(target_values[i]))
        if len(target_records) > 1:
            target_records = ' AND '.join(target_records)

        if len(target_fields) > 1:
            new_values = ', '.join(new_values)
            target_fields = ', '.join(target_fields)
        new_values = "(" + new_values + ")"
        target_fields = "(" + target_fields + ")"

        try:
            print(f'Updating index for {target_values} in table {tablename} . . .')
            query = f'''UPDATE {tablename}
                        SET {target_fields} = {new_values}
                        WHERE {target_records};'''
            self.cursor.execute(query)
            self.connection.commit()
            print(
                f'Successfully updated {target_fields} for {target_values} in {tablename} from {target_values} to {new_values}\n')
        except (Exception, Error) as error:
            print('There was an error:', error, "\n")

