from fastapi import APIRouter, Depends, Path

router = APIRouter(tags=["billing"], prefix="/billing")
