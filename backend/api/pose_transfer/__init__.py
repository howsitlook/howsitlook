"""
Pose Transfer API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, TokenData
from schemas.models import PoseTransferResponse
from services.pose_transfer_service import PoseTransferService
from schemas.base import PoseTransferResult
import logging
import tempfile
import os
import json
from core.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pose-transfer", tags=["Pose Transfer"])
settings = get_settings()


@router.post("/run", response_model=PoseTransferResponse)
async def run_pose_transfer(
    source_image: UploadFile = File(...),
    target_pose: str = Form(...),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfer target pose to source image.
    
    Args:
        source_image: Source person image
        target_pose: Target pose keypoints (JSON string)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Pose transfer result with image
    
    Raises:
        HTTPException: If pose transfer fails
    """
    try:
        user_id = int(current_user.subject)
        
        # Parse target pose
        try:
            target_pose_data = json.loads(target_pose)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid target_pose JSON"
            )
        
        # Save uploaded image temporarily
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, source_image.filename)
            with open(image_path, "wb") as f:
                content = await source_image.read()
                f.write(content)
            
            # Load image using service
            pose_service = PoseTransferService(
                model_type=settings.pose_transfer_model,
                device=settings.model_device
            )
            
            source_img = pose_service.load_image_from_file(image_path)
            
            # Run pose transfer
            result = await pose_service.transfer_pose(
                source_image=source_img,
                target_pose=target_pose_data,
                output_path=settings.output_dir
            )
        
        # Save result to database
        transfer_result = PoseTransferResult(
            user_id=user_id,
            source_image_path=image_path if os.path.exists(image_path) else None,
            target_pose=target_pose_data.get("keypoints", []),
            result_image_path=result["result_filepath"],
            confidence_score=result["confidence_score"],
            metadata=result["metadata"]
        )
        
        db.add(transfer_result)
        db.commit()
        db.refresh(transfer_result)
        
        logger.info(f"Pose transfer completed for user {user_id}")
        
        return PoseTransferResponse(
            id=transfer_result.id,
            user_id=user_id,
            result_image_url=result["result_base64"],
            confidence_score=result["confidence_score"],
            metadata=result["metadata"],
            created_at=transfer_result.created_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pose transfer failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Pose transfer failed"
        )


@router.get("/results/{transfer_id}", response_model=PoseTransferResponse)
async def get_pose_transfer_result(
    transfer_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a previous pose transfer result.
    
    Args:
        transfer_id: Pose transfer result ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Pose transfer result details
    
    Raises:
        HTTPException: If result not found or unauthorized
    """
    try:
        result = db.query(PoseTransferResult).filter(
            PoseTransferResult.id == transfer_id
        ).first()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pose transfer result {transfer_id} not found"
            )
        
        # Check authorization
        if result.user_id != int(current_user.subject):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own pose transfer results"
            )
        
        return PoseTransferResponse(
            id=result.id,
            user_id=result.user_id,
            result_image_url=result.result_image_path,
            confidence_score=result.confidence_score,
            metadata=result.metadata,
            created_at=result.created_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving pose transfer result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pose transfer result"
        )


@router.get("/my-results")
async def get_user_pose_transfer_results(
    skip: int = 0,
    limit: int = 20,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all pose transfer results for current user.
    
    Args:
        skip: Offset
        limit: Maximum results
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of pose transfer results
    """
    try:
        user_id = int(current_user.subject)
        
        total = db.query(PoseTransferResult).filter(
            PoseTransferResult.user_id == user_id
        ).count()
        
        results = db.query(PoseTransferResult).filter(
            PoseTransferResult.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [
                {
                    "id": r.id,
                    "result_image_url": r.result_image_path,
                    "confidence_score": r.confidence_score,
                    "created_at": r.created_at
                }
                for r in results
            ]
        }
    
    except Exception as e:
        logger.error(f"Error retrieving user pose transfer results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pose transfer results"
        )
