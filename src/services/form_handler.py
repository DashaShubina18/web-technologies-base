from src.schemas import UserSubmission
def handle_submission(data: UserSubmission):
    return {
        "message": f"Received data for {data.name}"
    }