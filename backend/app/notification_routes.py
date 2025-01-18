from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import FlightNotification
from .schemas import FlightNotificationCreate, FlightNotificationResponse
from .database import get_db
from .auth.dependencies import get_current_user  # Assuming you have a dependency for user authentication

router = APIRouter()

@router.post("/notify/notifications/", response_model=FlightNotificationResponse)
def create_notification(
    notification: FlightNotificationCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)  # Get current user
):
    """
    Create a new flight notification for the current user.
    """
    db_notification = FlightNotification(**notification.dict(), user_id=current_user.id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/notify/notifications/", response_model=list[FlightNotificationResponse])
def list_notifications(
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    """
    List all notifications for the current user.
    """
    notifications = db.query(FlightNotification).filter_by(user_id=current_user.id).all()
    return notifications

@router.delete("/notify/notifications/{notification_id}/")
def delete_notification(
    notification_id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    """
    Delete a specific notification by ID for the current user.
    """
    notification = db.query(FlightNotification).filter_by(id=notification_id, user_id=current_user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
