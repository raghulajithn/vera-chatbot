import mysql.connector
from datetime import datetime

# Initialize a global connection
global connection

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password='2110',
    database="taskdb"
)





def add_task(task_name, time, date):
    try:
        # Create a cursor
        cursor = connection.cursor()
        
        # Insert a new task into the "task" table
        insert_query = "INSERT INTO task (task_name, time, date) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (task_name, time, date))

        # Commit the changes
        connection.commit()

        return {"status": "Task added successfully"}

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"error": "Error adding the task. Please try again."}

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
            
def delete_task(task_name, time, date):
    try:
        # Create a cursor
        cursor = connection.cursor()

        # Delete the task from the "task" table
        delete_query = "DELETE FROM task WHERE task_name = %s AND time = %s AND date = %s"
        cursor.execute(delete_query, (task_name, time, date))

        # Commit the changes
        connection.commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return {"status": "Task deleted successfully"}
        else:
            return {"error": "Task not found"}

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"error": "Error deleting the task. Please try again."}

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
def view_task(parameters: dict):
    try:
        # Create a cursor
        cursor = connection.cursor(dictionary=True)

        # Construct the base query
        base_query = "SELECT task_name, time, date FROM task WHERE 1"

        date = parameters.get('date')
        # Build the WHERE clause based on the provided parameters
        if date and date.strip():  # Check if date is not an empty string after stripping whitespace
            base_query += f" AND date = '{date}'"

        # Execute the query
        cursor.execute(base_query)

        # Fetch the result
        result = cursor.fetchall()

        # Check if any rows were found
        if result:
            return {"fulfillment": result}
        else:
            date_readable = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
            return  f"No tasks found on {date_readable}"

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return {"error": f"Error viewing tasks: {err}"}

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# if __name__ == "__main__":
#     task_name_input = "Example Task"
#     time_input = "10:00"
#     date_input = "2024-01-17"

#     result = delete_task(task_name_input, time_input, date_input)

#     if 'error' in result:
#         print(f"Error: {result['error']}")
#     else:
#         print("Task added successfully")