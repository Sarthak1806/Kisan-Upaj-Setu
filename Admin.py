'''from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Kisan Upaj Setu backend is running"}'''
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date

from backend.app import (
    User,
    ProcurementCenter,
    ProcurementSlot,
    Booking,
    get_db,
    get_current_user
)


# =========================================================
# ADMIN ROUTER
# =========================================================

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class AdminCenterRequest(BaseModel):
    name: str
    district: str
    state: str
    address: str


class AdminSlotRequest(BaseModel):
    center_id: int
    crop_name: str
    procurement_date: str
    start_time: str
    end_time: str
    capacity: int


class BookingStatusRequest(BaseModel):
    status: str


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(
    current_user: User = Depends(get_current_user)
):
    """
    Allow access only to users whose role is admin.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


# =========================================================
# 1. CREATE PROCUREMENT CENTER
# =========================================================

@router.post("/centers")
def create_procurement_center(
    data: AdminCenterRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    # Check required fields
    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Center name is required"
        )

    if not data.district.strip():
        raise HTTPException(
            status_code=400,
            detail="District is required"
        )

    if not data.state.strip():
        raise HTTPException(
            status_code=400,
            detail="State is required"
        )

    if not data.address.strip():
        raise HTTPException(
            status_code=400,
            detail="Address is required"
        )

    center = ProcurementCenter(
        name=data.name.strip(),
        district=data.district.strip(),
        state=data.state.strip(),
        address=data.address.strip()
    )

    db.add(center)
    db.commit()
    db.refresh(center)

    return {
        "message": "Procurement center created successfully",
        "center": {
            "id": center.id,
            "name": center.name,
            "district": center.district,
            "state": center.state,
            "address": center.address
        }
    }


# =========================================================
# 2. CREATE PROCUREMENT SLOT
# =========================================================

@router.post("/slots")
def create_procurement_slot(
    data: AdminSlotRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    # -----------------------------------------------------
    # Check procurement center
    # -----------------------------------------------------

    center = db.query(ProcurementCenter).filter(
        ProcurementCenter.id == data.center_id
    ).first()

    if not center:
        raise HTTPException(
            status_code=404,
            detail="Procurement center not found"
        )

    # -----------------------------------------------------
    # Validate crop name
    # -----------------------------------------------------

    if not data.crop_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Crop name is required"
        )

    # -----------------------------------------------------
    # Validate capacity
    # -----------------------------------------------------

    if data.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    # -----------------------------------------------------
    # Validate date
    # -----------------------------------------------------

    try:
        selected_date = date.fromisoformat(
            data.procurement_date
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Date must be in YYYY-MM-DD format"
        )

    if selected_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Procurement date cannot be in the past"
        )

    # -----------------------------------------------------
    # Validate time
    # -----------------------------------------------------

    if not data.start_time.strip():
        raise HTTPException(
            status_code=400,
            detail="Start time is required"
        )

    if not data.end_time.strip():
        raise HTTPException(
            status_code=400,
            detail="End time is required"
        )

    # -----------------------------------------------------
    # Create slot
    # -----------------------------------------------------

    slot = ProcurementSlot(
        center_id=data.center_id,
        crop_name=data.crop_name.strip(),
        procurement_date=data.procurement_date,
        start_time=data.start_time.strip(),
        end_time=data.end_time.strip(),
        capacity=data.capacity,
        booked_count=0
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return {
        "message": "Procurement slot created successfully",
        "slot": {
            "id": slot.id,
            "center_id": slot.center_id,
            "center_name": center.name,
            "crop_name": slot.crop_name,
            "date": slot.procurement_date,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "capacity": slot.capacity,
            "booked": slot.booked_count,
            "available": slot.capacity
        }
    }


# =========================================================
# 3. ADMIN - VIEW ALL BOOKINGS
# =========================================================

@router.get("/bookings")
def get_all_bookings(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    bookings = db.query(Booking).all()

    result = []

    for booking in bookings:

        result.append({
            "booking_id": booking.id,
            "booking_code": booking.booking_code,

            "farmer": {
                "id": booking.farmer.id,
                "name": booking.farmer.name,
                "phone": booking.farmer.phone,
                "email": booking.farmer.email
            },

            "procurement": {
                "crop": booking.slot.crop_name,
                "quantity_quintal": booking.quantity_quintal,

                "center": booking.slot.center.name,
                "district": booking.slot.center.district,
                "state": booking.slot.center.state,

                "date": booking.slot.procurement_date,
                "start_time": booking.slot.start_time,
                "end_time": booking.slot.end_time
            },

            "status": booking.status,
            "payment_status": booking.payment_status
        })

    return {
        "total_bookings": len(result),
        "bookings": result
    }


# =========================================================
# 4. ADMIN - UPDATE BOOKING STATUS
# =========================================================

@router.put("/bookings/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    data: BookingStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Checked-in",
        "Completed",
        "Cancelled",
        "Rejected"
    ]

    # -----------------------------------------------------
    # Validate status
    # -----------------------------------------------------

    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid booking status",
                "allowed_statuses": allowed_statuses
            }
        )

    # -----------------------------------------------------
    # Find booking
    # -----------------------------------------------------

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    old_status = booking.status

    # -----------------------------------------------------
    # No change
    # -----------------------------------------------------

    if old_status == data.status:
        return {
            "message": "Booking status is already set",
            "booking_id": booking.id,
            "booking_code": booking.booking_code,
            "status": booking.status
        }

    # -----------------------------------------------------
    # Active -> Cancelled / Rejected
    #
    # Free one slot capacity
    # -----------------------------------------------------

    if (
        old_status not in ["Cancelled", "Rejected"]
        and data.status in ["Cancelled", "Rejected"]
    ):

        if booking.slot.booked_count > 0:
            booking.slot.booked_count -= 1

    # -----------------------------------------------------
    # Cancelled / Rejected -> Active
    #
    # Occupy one slot capacity
    # -----------------------------------------------------

    elif (
        old_status in ["Cancelled", "Rejected"]
        and data.status in ["Pending", "Confirmed"]
    ):

        if booking.slot.booked_count >= booking.slot.capacity:
            raise HTTPException(
                status_code=400,
                detail="Cannot confirm booking. Slot is full."
            )

        booking.slot.booked_count += 1

    # -----------------------------------------------------
    # Update status
    # -----------------------------------------------------

    booking.status = data.status

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking status updated successfully",

        "booking": {
            "id": booking.id,
            "booking_code": booking.booking_code,
            "old_status": old_status,
            "new_status": booking.status,
            "slot_id": booking.slot_id,
            "slot_booked": booking.slot.booked_count,
            "slot_available": max(
                booking.slot.capacity -
                booking.slot.booked_count,
                0
            )
        }
    }
 