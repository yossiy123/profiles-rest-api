import os
import sqlite3

import random

from timestemp import TimeStemp
from logger import logger
from logger import LogType

class MySqliteDataBase:
    """
    Database Class
    After init please verify database_create's value is True, else somthing went worng. 
    """

    _ENDS_WITH = '.sqlite3'

    def __init__(self, i_database_file_name, i_override = False, i_save_copy = True, i_save_deleted_tables = True):
        """
        Init:
        database_file_name (String): name of the file, most end with '.sqlite3'.
        override (Boolean): override the file if it's already exists.
        save_copy (Boolean): if 'override' is True, before delete the old database save it if this field is True, else delete it.
        """

        self.database_created = True
        self._save_deleted_tables = i_save_deleted_tables
        self.failed_messages = []
        self._init_connection()
        self._init_cursor()

        if ((self.database_created) and (not self._set_database_file_name(i_database_file_name = i_database_file_name))):
            self.database_created = False
            self.add_log_to_failed_list(i_message = '_set_database_file_name failed')
        
        if ((self.database_created) and (not self._database_file_init(i_database_file_name = i_database_file_name, i_override = i_override, i_save_copy = i_save_copy))):
            self.database_created = False
            self.add_log_to_failed_list(i_message = '_database_file_init failed')
        
        if ((self.database_created) and (not self.open_connection())):
            self.database_created = False
            self.add_log_to_failed_list(i_message = 'open_connection failed')
        
        if ((self.database_created) and (not self._set_cursor(self.get_connection().cursor()))):
            self.database_created = False
            self.add_log_to_failed_list(i_message = '_set_cursor failed')

        self.log_failed_message()

    def _database_file_init(self, i_database_file_name, i_override = False, i_save_copy = True):
        logger.write_info_log(i_message = '_database_file_init')
        try:
            if (os.path.exists(i_database_file_name)):
                logger.write_info_log(i_message = 'File Exists')
                if (i_override):
                    logger.write_info_log(i_message = 'Override')
                    if (i_save_copy):
                        logger.write_info_log(i_message = 'Save Copy')
                        os.rename(i_database_file_name, 
                                    TimeStemp.get_time_stemp() + '_' + i_database_file_name)
                    else:
                        logger.write_info_log(i_message = 'Not Save Copy')
                        os.remove(i_database_file_name)
                    logger.write_info_log(i_message = 'File removed!')
                else:
                    logger.write_info_log(i_message = 'Not Override!')
            else:
                logger.write_info_log(i_message = "FILE NOT EXIST!")


            is_init = True
        except Exception as ee:
            is_init = False
            self.add_log_to_failed_list(i_message = str(ee))
        
        return is_init

    def _create_file(self, i_database_file_name):
        pass

    def _set_database_file_name(self, i_database_file_name):
        """
        Set database file name.
        database_file_name (String): string most ends with '.sqlite3'
        Return Boolean
        True - Ok.
        False - File name does not match the conditions.
        """

        is_file_name_set = False
        if (i_database_file_name.endswith(MySqliteDataBase._ENDS_WITH)):
            is_file_name_set = True
            self.m_database_file_name = i_database_file_name
        else:
            is_file_name_set = False
            self.add_log_to_failed_list(i_message = f'Bad file name format, not ends with "{MySqliteDataBase._ENDS_WITH}".')
        
        return is_file_name_set

    def get_database_file_name(self):
        return self.m_database_file_name
    
    def _init_connection(self):
        self._set_connection(i_connection = None)

    def log_failed_message(self):
        for msg in self.failed_messages:
            logger.write_error_log(i_message = msg)
        self.failed_messages = []

    def _set_connection(self, i_connection):
        self.m_database_connection = i_connection
        return True

    def get_connection(self):
        return self.m_database_connection
    
    def _init_cursor(self):
        return self._set_cursor(i_cursor = None)

    def _set_cursor(self, i_cursor):
        self.m_cursor = i_cursor
        return True
    
    def get_cursor(self):
        return self.m_cursor

    def open_connection(self):
        connection_opened = False
        try:
            #self. database_connection = sqlite3.connect(self.m_database_file_name)
            aa = sqlite3.connect(self.m_database_file_name)
            aa.row_factory = sqlite3.Row
            self._set_connection(aa)
            connection_opened = True
        except Exception as ee:
            #self. database_connection = None
            self._set_connection(None)
            connection_opened = False
            self.add_log_to_failed_list(i_message = 'sqlite3.connect failed with error: ' + str(ee))
        return connection_opened

    def close_connection(self):
        #if (self. database_connection):
        if (self.get_connection()):
            try:
                #self. database_connection.close()
                self.get_connection().close()
                logger.write_info_log(i_message = "SQLite connection closed")
            except Exception as ee:
                logger.write_error_log(i_message = str(ee))

    def check_table_exist(self, i_table_name):
        if (not self.database_created):
            logger.write_error_log(i_message = 'Database is not available')
            return False
        
        print(len(self._execute_query(f"""SELECT COUNT(*) FROM {i_table_name};""")))

    def insert_row(self, i_table_name, i_values):
        if (not self.database_created):
            logger.write_error_log(i_message = 'Database is not available')
            return False
        
        query = f"""INSERT INTO {i_table_name} values ({', '.join(i_values)});"""
        return self._save_execute_query(i_query = query, i_function_called = 'insert_row', i_call_at_end = self.save_connection)

        #if (not  self._execute_query(i_query = query)):
        #    self.add_log_to_failed_list(i_message = '_execute_query failed')
        #    self.log_failed_message()
        #else:
        #    self.save_connection()

    def delete_row(self, i_table_name, i_id):

        query = f"""DELETE FROM {i_table_name} WHERE id={i_id}"""
        
        return self._save_execute_query(i_query = query, i_function_called = 'delete_row', i_call_at_end = self.save_connection)
        #if (not  self._execute_query(i_query = query)):
        #    table_renamed = False
        #    self.add_log_to_failed_list(i_message = 'rename_table failed')
        #    self.log_failed_message()
        #else:
        #    table_renamed = True
        #return table_renamed

    def update_row(self, i_table_name, i_id, i_new_values):
        """
        Update a row for specipic ID.
        table_name: Table to update.
        id: ID of row.
        new_values: The columns name and new value like: <COLUMN_NAME>=<NEW_VALUE> 
        """
        query = f"""UPDATE {i_table_name} SET {', '.join(i_new_values)} WHERE id={i_id};"""

        return self._save_execute_query(i_query = query, i_function_called = 'update_row', i_call_at_end = self.save_connection)

    def _save_execute_query(self, i_query, i_function_called, i_call_at_end = None):
        execute_succeeded = False
        object_to_return = self._execute_query(i_query = i_query)
        if (object_to_return is None):
            object_to_return = False
            self.add_log_to_failed_list(i_message = i_function_called + ' failed')
            self.log_failed_message()
        else:
            execute_succeeded = True
            if (i_call_at_end is not None):
                i_call_at_end()
        
        return object_to_return

    def create_new_table(self, i_new_table_name, i_columns_name):
        if (not self.database_created):
            logger.write_error_log(i_message = 'Database is not available')
            return False
        query = f'CREATE TABLE {i_new_table_name} ({", ".join(i_columns_name)});'
        self._save_execute_query(i_query = query, i_function_called = 'create_new_table', i_call_at_end = self.save_connection)

    def sql_object_to_list_of_dict(self, i_sql_object):
        sql_result_in_list = list([])

        for row_object in i_sql_object.fetchall():
            sql_result_in_list.append(dict(row_object))
        
        return sql_result_in_list

    def add_log_to_failed_list(self, i_message):
        self.failed_messages.insert(0, i_message)

    def delete_table(self, i_table_name):
        table_deleted = False
        if (self._save_deleted_tables):
            if (not self.rename_table(i_old_table_name = i_table_name, i_new_table_name = i_table_name + "_deleted")):
                table_deleted = False
                self.add_log_to_failed_list(i_message = 'delete_table failed')
                self.log_failed_message()
            else:
                table_deleted = True
        else:
            table_deleted = self._save_execute_query(i_query = query, i_function_called = 'delete_table')
        #else if (not  self._execute_query(i_query = query)):
        #    query = f"""DROP TABLE {i_table_name};"""
        #    table_deleted = False
        #    self.add_log_to_failed_list(i_message = 'delete_table failed')
        #    self.log_failed_message()
        #else:
        #    table_deleted = True
        
        return table_deleted

    def rename_table(self, i_old_table_name, i_new_table_name):

        query = f"""ALTER TABLE {i_old_table_name} RENAME TO {i_new_table_name};"""
        
        return self._save_execute_query(i_query = query, i_function_called = 'rename_table')
        #if (not  self._execute_query(i_query = query)):
        #    table_renamed = False
        #    self.add_log_to_failed_list(i_message = 'rename_table failed')
        #    self.log_failed_message()
        #else:
        #    table_renamed = True
        #return table_renamed

    def save_connection(self):
        self.get_connection().commit()

    def get_columns_names(self, i_table_name):
        column_names = list([])
        query = f"SELECT * FROM {i_table_name} AS tt"
        sql_result = self._save_execute_query(i_query = query, i_function_called = 'get_columns_names')

        print([f[0] for f in sql_result.description])
        if (sql_result is not None):
            fetchone_result = sql_result.fetchone()
            if (fetchone_result is not None):
                column_names = sql_result.fetchone().keys()
        
        return column_names

    def _execute_query(self, i_query):
        execute_succeeded = None
        try:
            execute_succeeded = self.get_cursor().execute(i_query)
        except Exception as ee:
            self.add_log_to_failed_list(i_message = '_execute_query failed with error: ' + str(ee))
            execute_succeeded = None

        return execute_succeeded

    def __str__(self):
        return ((self.m_database_file_name) if (self.database_created) else ('Database not created!'))
    
    def __del__(self):
        self.close_connection()

if (__name__ == '__main__'):
    db = MySqliteDataBase('ff'+MySqliteDataBase._ENDS_WITH)
    logger.write_info_log(i_message = db)

    while(True):
        inpt = input('Plaese enter 1 for create table or 2 to check if exists: ')
        try:
            inpt = int(inpt)
        except Exception as ee:
            print('Not int, try again!')
            continue

        if (inpt == 0):
            break
        if (inpt == 1):
            db.create_new_table(i_new_table_name = 'ff', i_columns_name = ['aa', 'bb'])
        if (inpt == 2):
            db.check_table_exist(i_table_name = 'ff')
        if (inpt == 3):
            db.insert_row(i_table_name = 'ff', i_values = [str(int(random.random() * 10)), str(int(random.random() * 10))])
        if (inpt == 4):
            aa = input("Please enter value fore 'aa': ")
            dddd = db._save_execute_query(i_query = f'SELECT * FROM "ff" as ff WHERE ff.aa = {aa}', i_function_called = 'temp')
            for item in db.sql_object_to_list_of_dict(dddd):
                print(item)
        if (inpt == 5):
            print(', '.join(db.get_columns_names(i_table_name = 'ff')))
                


        