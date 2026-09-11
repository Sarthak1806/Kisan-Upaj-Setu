from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel, EmailStr
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

from jose import jwt, JWTError
from uuid import uuid4
import hashlib
import os


# =========================================================
# APP CONFIGURATION
# =========================================================

app = FastAPI(
    title="Kisan Upaj Setu API",
    description="Smart Procurement System for Farmers",
    version="1.0.0"
)


# =========================================================
# CORS
# Frontend can communicate with backend
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = "postgresql+psycopg://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/farmer_procurement"

engine = create_engine(
    DATABASE_URL
    
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "KISAN_UPAJ_SETU_CHANGE_THIS_SECRET_KEY"
)

ALGORITHM = "HS256"

security = HTTPBearer()


def hash_password(password: str):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_token(user_id: int):

    return jwt.encode(
        {
            "sub": str(user_id)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================================================
# DATABASE MODELS
# =========================================================


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=True
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="farmer"
    )

    bookings = relationship(
        "Booking",
        back_populates="farmer"
    )


class ProcurementCenter(Base):

    __tablename__ = "procurement_centers"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    district = Column(
        String,
        nullable=False
    )

    state = Column(
        String,
        nullable=False
    )

    address = Column(
        String
    )

    slots = relationship(
        "ProcurementSlot",
        back_populates="center"
    )


class ProcurementSlot(Base):

    __tablename__ = "procurement_slots"

    id = Column(
        Integer,
        primary_key=True
    )

    center_id = Column(
        Integer,
        ForeignKey("procurement_centers.id")
    )

    crop_name = Column(
        String,
        nullable=False
    )

    procurement_date = Column(
        String,
        nullable=False
    )

    start_time = Column(
        String,
        nullable=False
    )

    end_time = Column(
        String,
        nullable=False
    )

    capacity = Column(
        Integer,
        default=20
    )

    booked_count = Column(
        Integer,
        default=0
    )

    center = relationship(
        "ProcurementCenter",
        back_populates="slots"
    )

    bookings = relationship(
        "Booking",
        back_populates="slot"
    )


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True
    )

    booking_code = Column(
        String,
        unique=True
    )

    farmer_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    slot_id = Column(
        Integer,
        ForeignKey("procurement_slots.id")
    )

    quantity_quintal = Column(
        Float
    )

    status = Column(
        String,
        default="Confirmed"
    )

    payment_status = Column(
        String,
        default="Pending"
    )

    payment_amount = Column(
        Float,
        default=0
    )

    farmer = relationship(
        "User",
        back_populates="bookings"
    )

    slot = relationship(
        "ProcurementSlot",
        back_populates="bookings"
    )


# Create database tables

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# PYDANTIC REQUEST MODELS
# =========================================================


class RegisterRequest(BaseModel):

    name: str

    phone: str

    email: EmailStr | None = None

    password: str


class LoginRequest(BaseModel):

    phone: str

    password: str


class CenterRequest(BaseModel):

    name: str

    district: str

    state: str

    address: str


class SlotRequest(BaseModel):

    center_id: int

    crop_name: str

    procurement_date: str

    start_time: str

    end_time: str

    capacity: int


class BookingRequest(BaseModel):

    slot_id: int

    quantity_quintal: float


# =========================================================
# CURRENT USER
# =========================================================


def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(security),

    db: Session = Depends(get_db)

):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(
            payload.get("sub")
        )

    except (JWTError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# =========================================================
# HOME API
# =========================================================


@app.get("/")

def home():

    return {

        "message": "Welcome to Kisan Upaj Setu API",

        "status": "Running"

    }


# =========================================================
# REGISTER FARMER
# =========================================================


@app.post("/auth/register")

def register_user(

    data: RegisterRequest,

    db: Session = Depends(get_db)

):

    existing_user = db.query(User).filter(
        User.phone == data.phone
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )

    if data.email:

        existing_email = db.query(User).filter(
            User.email == data.email
        ).first()

        if existing_email:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    user = User(

        name=data.name,

        phone=data.phone,

        email=data.email,

        password=hash_password(
            data.password
        )

    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_token(
        user.id
    )

    return {

        "message": "Farmer registered successfully",

        "access_token": token,

        "user": {

            "id": user.id,

            "name": user.name,

            "phone": user.phone

        }

    }


# =========================================================
# LOGIN
# =========================================================


@app.post("/auth/login")

def login(

    data: LoginRequest,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(
        User.phone == data.phone
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid phone number or password"
        )

    if user.password != hash_password(
        data.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid phone number or password"
        )

    token = create_token(
        user.id
    )

    return {

        "message": "Login successful",

        "access_token": token,

        "user": {

            "id": user.id,

            "name": user.name,

            "role": user.role

        }

    }


# =========================================================
# GET PROCUREMENT CENTERS
# =========================================================


@app.get("/centers")

def get_centers(

    db: Session = Depends(get_db)

):

    centers = db.query(
        ProcurementCenter
    ).all()

    return centers


# =========================================================
# CREATE PROCUREMENT CENTER
# =========================================================


@app.post("/centers")

def create_center(

    data: CenterRequest,

    db: Session = Depends(get_db)

):

    center = ProcurementCenter(

        name=data.name,

        district=data.district,

        state=data.state,

        address=data.address

    )

    db.add(center)

    db.commit()

    db.refresh(center)

    return {

        "message": "Procurement center created",

        "center_id": center.id

    }


# =========================================================
# GET PROCUREMENT SLOTS
# =========================================================


@app.get("/slots")

def get_slots(

    center_id: int | None = None,

    db: Session = Depends(get_db)

):

    query = db.query(
        ProcurementSlot
    )

    if center_id:

        query = query.filter(
            ProcurementSlot.center_id == center_id
        )

    slots = query.all()

    result = []

    for slot in slots:

        result.append({

            "id": slot.id,

            "center_name": slot.center.name,

            "crop_name": slot.crop_name,

            "date": slot.procurement_date,

            "start_time": slot.start_time,

            "end_time": slot.end_time,

            "capacity": slot.capacity,

            "booked": slot.booked_count,

            "available": (
                slot.capacity
                -
                slot.booked_count
            )

        })

    return result


# =========================================================
# CREATE PROCUREMENT SLOT
# =========================================================


@app.post("/slots")

def create_slot(

    data: SlotRequest,

    db: Session = Depends(get_db)

):

    center = db.query(
        ProcurementCenter
    ).filter(

        ProcurementCenter.id
        ==
        data.center_id

    ).first()

    if not center:

        raise HTTPException(
            status_code=404,
            detail="Procurement center not found"
        )

    slot = ProcurementSlot(

        center_id=data.center_id,

        crop_name=data.crop_name,

        procurement_date=data.procurement_date,

        start_time=data.start_time,

        end_time=data.end_time,

        capacity=data.capacity

    )

    db.add(slot)

    db.commit()

    db.refresh(slot)

    return {

        "message": "Slot created successfully",

        "slot_id": slot.id

    }


# =========================================================
# BOOK PROCUREMENT SLOT
# =========================================================


@app.post("/bookings")

def book_slot(

    data: BookingRequest,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    slot = db.query(
        ProcurementSlot
    ).filter(

        ProcurementSlot.id
        ==
        data.slot_id

    ).first()

    if not slot:

        raise HTTPException(
            status_code=404,
            detail="Slot not found"
        )

    if slot.booked_count >= slot.capacity:

        raise HTTPException(
            status_code=400,
            detail="This slot is already full"
        )

    booking = Booking(

        booking_code=
        "KUS-"
        +
        uuid4().hex[:8].upper(),

        farmer_id=current_user.id,

        slot_id=data.slot_id,

        quantity_quintal=data.quantity_quintal,

        status="Confirmed",

        payment_status="Pending"

    )

    slot.booked_count += 1

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return {

        "message": "Procurement slot booked successfully",

        "booking_id": booking.id,

        "booking_code": booking.booking_code,

        "status": booking.status

    }


# =========================================================
# GET MY BOOKINGS
# =========================================================


@app.get("/bookings/my")

def my_bookings(

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    bookings = db.query(
        Booking
    ).filter(

        Booking.farmer_id
        ==
        current_user.id

    ).all()

    result = []

    for booking in bookings:

        result.append({

            "booking_code":
            booking.booking_code,

            "crop":
            booking.slot.crop_name,

            "center":
            booking.slot.center.name,

            "date":
            booking.slot.procurement_date,

            "time":
            booking.slot.start_time,

            "quantity":
            booking.quantity_quintal,

            "status":
            booking.status,

            "payment_status":
            booking.payment_status

        })

    return result


# =========================================================
# FARMER DASHBOARD
# =========================================================


@app.get("/dashboard")

def farmer_dashboard(

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    bookings = db.query(
        Booking
    ).filter(

        Booking.farmer_id
        ==
        current_user.id

    ).all()

    total_quantity = sum(
        booking.quantity_quintal
        for booking in bookings
    )

    confirmed = len([

        booking

        for booking in bookings

        if booking.status == "Confirmed"

    ])

    next_slot = None

    if bookings:

        booking = bookings[-1]

        next_slot = {

            "crop":
            booking.slot.crop_name,

            "center":
            booking.slot.center.name,

            "date":
            booking.slot.procurement_date,

            "time":
            booking.slot.start_time

        }

    return {

        "farmer_name":
        current_user.name,

        "total_bookings":
        len(bookings),

        "confirmed_bookings":
        confirmed,

        "total_quantity_quintals":
        total_quantity,

        "next_procurement":
        next_slot

    }


# =========================================================
# HEALTH CHECK
# =========================================================


@app.get("/health")

def health():

    return {

        "status": "healthy",

        "project": "Kisan Upaj Setu"

    }