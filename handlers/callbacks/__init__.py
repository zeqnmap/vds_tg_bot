from .social_b import router as social_router
from .study_b import router as study_router
from .transport_b import router as transport_router
from .usual_b import router as usual_router
from .unusual_b import router as unusual_router
from .back_b import router as back_router

__all__ = [
    'social_router',
    'study_router',
    'transport_router',
    'usual_router',
    'unusual_router',
    'back_router'
]

from aiogram import Router

main_callback_router = Router()

main_callback_router.include_router(social_router)
main_callback_router.include_router(study_router)
main_callback_router.include_router(transport_router)
main_callback_router.include_router(usual_router)
main_callback_router.include_router(unusual_router)
main_callback_router.include_router(back_router)