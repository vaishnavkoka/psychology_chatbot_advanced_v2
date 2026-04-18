"""
Report Generation Endpoints and Integration
Adds report generation capabilities to the FastAPI backend
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, List
import logging
from datetime import datetime
from pathlib import Path

# This would be imported when integrated into backend.py
# from utils.report_generator import ReportGenerator, generate_report

logger = logging.getLogger(__name__)

# Request models
class ReportRequest(BaseModel):
    """Request model for report generation"""
    session_id: str
    include_pdf: bool = True
    include_json: bool = True
    include_analytics: bool = True

class ReportMetadata(BaseModel):
    """Report metadata"""
    session_id: str
    generated_at: str
    format: str
    file_path: str


# Router for report endpoints
def create_report_router(app_instance=None):
    """Create report router for integration into FastAPI app"""
    
    router = APIRouter(prefix="/reports", tags=["reports"])
    
    @router.post("/generate")
    async def generate_session_report(
        request: ReportRequest,
        background_tasks: BackgroundTasks
    ):
        """
        Generate comprehensive session report
        
        Args:
            request: Report generation request
            background_tasks: FastAPI background tasks
            
        Returns:
            Report generation status and file paths
        """
        try:
            logger.info(f"Generating report for session: {request.session_id}")
            
            # This would be real data from session management
            conversation_history = []
            orchestrator_results = []
            crisis_events = []
            
            # Generate report
            from utils.report_generator import generate_report
            
            report_paths = generate_report(
                session_id=request.session_id,
                conversation_history=conversation_history,
                orchestrator_results=orchestrator_results,
                crisis_events=crisis_events,
                output_dir="reports"
            )
            
            return {
                "success": True,
                "session_id": request.session_id,
                "reports": report_paths,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/list")
    async def list_reports():
        """List all generated reports"""
        try:
            reports_dir = Path("reports")
            if not reports_dir.exists():
                return {"reports": [], "total": 0}
            
            reports = list(reports_dir.glob("report_*.json"))
            
            report_info = []
            for report_path in sorted(reports, reverse=True)[:20]:  # Last 20
                report_info.append({
                    "filename": report_path.name,
                    "path": str(report_path),
                    "created": datetime.fromtimestamp(report_path.stat().st_mtime).isoformat(),
                    "size_bytes": report_path.stat().st_size
                })
            
            return {
                "reports": report_info,
                "total": len(reports)
            }
        except Exception as e:
            logger.error(f"Error listing reports: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/download/{report_id}")
    async def download_report(report_id: str):
        """Download a specific report"""
        try:
            report_path = Path("reports") / report_id
            
            if not report_path.exists():
                raise HTTPException(status_code=404, detail="Report not found")
            
            with open(report_path, 'r') as f:
                content = f.read()
            
            return {
                "success": True,
                "report_id": report_id,
                "content": content
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error downloading report: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/{session_id}/summary")
    async def get_report_summary(session_id: str):
        """Get summary of a specific session's reports"""
        try:
            reports_dir = Path("reports")
            matching_reports = list(reports_dir.glob(f"*{session_id}*"))
            
            if not matching_reports:
                raise HTTPException(status_code=404, detail="No reports found for session")
            
            summaries = []
            for report_path in matching_reports:
                try:
                    import json
                    with open(report_path, 'r') as f:
                        report = json.load(f)
                    
                    summary = {
                        "filename": report_path.name,
                        "generated_at": report.get("metadata", {}).get("generated_at"),
                        "total_messages": report.get("session_summary", {}).get("total_messages", 0),
                        "crisis_detected": report.get("session_summary", {}).get("crisis_detected", False),
                        "primary_topics": report.get("session_summary", {}).get("primary_topics", [])
                    }
                    summaries.append(summary)
                except Exception as e:
                    logger.warning(f"Error reading report {report_path}: {e}")
                    continue
            
            return {
                "session_id": session_id,
                "reports": summaries,
                "total": len(summaries)
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting report summary: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.delete("/{report_id}")
    async def delete_report(report_id: str):
        """Delete a specific report"""
        try:
            report_path = Path("reports") / report_id
            
            if not report_path.exists():
                raise HTTPException(status_code=404, detail="Report not found")
            
            report_path.unlink()
            
            return {
                "success": True,
                "message": f"Report {report_id} deleted",
                "deleted_at": datetime.now().isoformat()
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting report: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return router


# Integration instructions for backend.py
"""
To integrate reports into backend.py, add the following:

1. Import at the top:
   from report_routes import create_report_router
   
2. After creating FastAPI app, add the router:
   report_router = create_report_router(app)
   app.include_router(report_router)
   
3. In lifespan startup, initialize report directory:
   global report_generator
   from utils.report_generator import ReportGenerator
   report_generator = ReportGenerator(output_dir="reports")
   logger.info("✅ Report generator initialized")
   
4. When sending chat response, track for reporting:
   # Save conversation turn for report generation
   st.session_state.conversation_history.append({
       "role": "user",
       "content": user_input
   })
   st.session_state.conversation_history.append({
       "role": "assistant",
       "content": response_text,
       "agent": agent_used,
       "crisis_detected": crisis_detected
   })
"""
