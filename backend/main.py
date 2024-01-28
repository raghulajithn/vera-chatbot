from fastapi import FastAPI, HTTPException
from db_handler import add_task, delete_task, view_task
from datetime import datetime

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request_body: dict):
    try:
        # Extract parameters and session_id from the webhook request
        query_result = request_body["queryResult"]
        parameters = query_result.get("parameters", {})
        session_id = query_result.get("outputContexts", [])[0].get("parameters", {}).get("session_id")

        intent_name = query_result["intent"]["displayName"]

        # Dispatch to the appropriate function based on the intent
        if intent_name == "new.task":
            return create_new_task(parameters)
        elif intent_name == "delete.task - context:ongoing-task":
            return remove_task(parameters)
        elif intent_name == "view.task":
            return task_view(parameters)
        else:
            raise HTTPException(status_code=400, detail="Unsupported intent")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_new_task(parameters: dict):
    # Your logic for handling "new task" intent
    task_name = parameters.get("task")
    time = parameters.get("time")
    date = parameters.get("date")
    
    # convert date and time to mysql format
    parsed_timestamp = datetime.fromisoformat(time)
    time = parsed_timestamp.strftime('%H:%M:%S')

    parsed_timestamp = datetime.fromisoformat(date)
    date = parsed_timestamp.strftime('%Y-%m-%d')
    
    print(task_name)
    print(time)
    print(date)
    
    task_info = add_task(task_name, time, date)
    
    # convert date and time to common format
    time = datetime.strptime(time, '%H:%M:%S').strftime('%I:%M %p')
    date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    
    if 'error' in task_info:
        response_text = f"Error: {task_info['error']}"
    else:
        response_text = f"Created a new task {task_name} on {date} at {time} ! Anything else? "
    return {"fulfillmentText": response_text}

from datetime import datetime

def remove_task(parameters: dict):
    try:
        # Extract task information from parameters
        task_name = parameters.get("task")
        time = parameters.get("time")
        date = parameters.get("date")
    
        # Convert date and time to MySQL format
        parsed_timestamp = datetime.fromisoformat(time)
        time = parsed_timestamp.strftime('%H:%M:%S')

        parsed_timestamp = datetime.fromisoformat(date)
        date = parsed_timestamp.strftime('%Y-%m-%d')

    
        # Call the delete_task function from db_handler
        task_info = delete_task(task_name, time, date)
    
        # Convert date and time to common format
        time_readable = datetime.strptime(time, '%H:%M:%S').strftime('%I:%M %p')
        date_readable = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    
        if 'error' in task_info:
            response_text = f"Error: {task_info['error']}"
        else:
            response_text = f"Removed the task {task_name} scheduled for {date_readable} at {time_readable} . Anything else?"
        
        return {"fulfillmentText": response_text}

    except Exception as e:
        return {"fulfillmentText": f"Error removing the task: {str(e)}"}

def task_view(parameters: dict):
    try:
        # Extract task information from parameters
        date = parameters.get("date")

        # Convert date to MySQL format
        if date:
            parsed_timestamp = datetime.fromisoformat(date)
            date = parsed_timestamp.strftime('%Y-%m-%d')

        # Call the view_task function from db_handler
        task_info = view_task({"date": date})

        # Convert date to common format
        if date:
            date_readable = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

        if 'error' in task_info:
            response_text = f"Error: {task_info['error']}"
        elif 'fulfillment' in task_info and task_info['fulfillment']:
            # Customize the response based on the available information
            tasks = task_info['fulfillment']
            response_text = f"Tasks"
            if date:
                response_text += f" on {date_readable}"
            response_text += ":\n"
            response_text += "\n".join([f"{task['task_name']} at {datetime.strptime(str(task['time']), '%H:%M:%S').strftime('%I:%M %p')} on {datetime.strptime(str(task['date']), '%Y-%m-%d').strftime('%d/%m/%Y')}. " for task in tasks])
            response_text += "\n Anything else?"
        else:
            response_text = f"No tasks found"
            if date:
                response_text += f" on {date_readable}!! Anything else?"

        print(response_text)

        return {"fulfillmentText": response_text}

    except Exception as e:
        return {"fulfillmentText": f"Error viewing tasks: {str(e)}"}
 
async def root():
    return {"message": "Hello World"}