from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import ollama

from app.database import get_db
from app.models.chat_history import ChatHistory
from app.models.user import User
from app.schemas.chat_schema import ChatRequest

router = APIRouter()


# Ollama connection
client = ollama.Client(
    host="http://127.0.0.1:11434"
)


SYSTEM_PROMPT = """
You are a Medical Assistant AI for a student project.

Your role is to provide general health and wellness information.

Rules:
1. Give clear, simple and helpful answers.
2. Do not claim to diagnose diseases.
3. Do not prescribe medicines or prescription dosages.
4. For severe or emergency symptoms, advise the user to seek
   immediate professional medical care.
5. Encourage users to consult a qualified healthcare professional
   for diagnosis and treatment.
6. For diet and lifestyle questions, provide practical general suggestions.
7. Never pretend to be a doctor.
8. Keep answers concise and easy to understand.
"""


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == request.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Ask Ollama
    try:
        print("User ID:", request.user_id)
        print("Question:", request.message)

        response = client.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        print("Ollama response:", response)

        ai_response = response["message"]["content"]

    except Exception as e:
        print("OLLAMA ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Ollama error: {str(e)}"
        )

    # Save chat history
    try:
        chat_record = ChatHistory(
            user_id=request.user_id,
            question=request.message,
            response=ai_response
        )

        db.add(chat_record)
        db.commit()
        db.refresh(chat_record)

    except Exception as e:
        db.rollback()

        print("DATABASE ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    return {
        "message": request.message,
        "response": ai_response,
        "chat_id": chat_record.id
    }

@router.get("/chat/history/{user_id}")
def get_chat_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    try:
        history = (
            db.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_at.desc())
            .all()
        )

        return {
            "user_id": user_id,
            "history": [
                {
                    "id": chat.id,
                    "question": chat.question,
                    "response": chat.response,
                    "created_at": chat.created_at
                }
                for chat in history
            ]
        }

    except Exception as e:
        print("HISTORY ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )