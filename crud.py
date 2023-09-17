from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from models import Doctor, Patient
from schema import DoctorCreate, DoctorUpdate, PatientCreate, PatientUpdate
import logging


# Asynchronous CRUD operations for Doctors
async def add_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    return new_doctor


async def get_doctors(db: Session):
    result = await db.execute(select(Doctor))
    return result.scalars().all()


async def get_single_doctor(db: Session, doctor_id: int):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


async def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    doctor = await get_single_doctor(db, doctor_id)
    for key, value in doctor_data.model_dump().items():
        setattr(doctor, key, value)
    await db.commit()
    await db.refresh(doctor)
    return doctor


async def delete_doctor(db: Session, doctor_id: int):
    logging.basicConfig(level=logging.INFO)
    doctor = await get_single_doctor(db, doctor_id)
    # Check if doctor exists
    if not doctor:
        logging.info(f"No doctor found with id: {doctor_id}")
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        # Delete the doctor
        await db.delete(doctor)
        await db.flush()
        logging.info(f"Flushed the delete operation for doctor id: {doctor_id}")
    except Exception as e:
        logging.error(f"An error occurred while deleting doctor: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        # Commit the transaction
        await db.commit()
        logging.info(f"Committed the delete operation for doctor id: {doctor_id}")
        return {"message": "Doctor deleted successfully"}
    except Exception as e:
        logging.error(f"An error occurred while committing the transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Asynchronous CRUD operations for Patients
async def add_patient(db: Session, patient: PatientCreate) -> Patient:
    new_patient = Patient(**patient.model_dump())
    db.add(new_patient)
    await db.flush()
    await db.commit()
    await db.refresh(new_patient)
    return new_patient


async def get_patients(db: Session):
    result = await db.execute(select(Patient))
    return result.scalars().all()


async def get_single_patient(db: Session, patient_id: int):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


async def update_patient(db: Session, patient_id: int, patient_data: PatientUpdate):
    patient = await get_single_patient(db, patient_id)
    for key, value in patient_data.model_dump().items():
        setattr(patient, key, value)
    await db.commit()
    await db.refresh(patient)
    return patient


async def delete_patient(db: Session, patient_id: int):
    patient = await get_single_patient(db, patient_id)
    await db.delete(patient)
    await db.commit()
    return {"message": "Patient deleted successfully"}

