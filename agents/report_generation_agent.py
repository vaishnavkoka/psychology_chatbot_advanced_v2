"""
Report Generation Agent - Creates comprehensive psychology assessment reports
Supports PDF, JSON, and CSV export formats
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging
from enum import Enum
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
except ImportError:
    print("Installing reportlab for PDF generation...")
    import os
    os.system("pip install reportlab -q")
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch

logger = logging.getLogger(__name__)

class ReportFormat(str, Enum):
    """Supported report formats"""
    PDF = "pdf"
    JSON = "json"
    CSV = "csv"


class ReportGenerationAgent:
    """Generates comprehensive psychology assessment reports"""
    
    def __init__(self):
        self.formats = [fmt.value for fmt in ReportFormat]
        logger.info("✅ Report Generation Agent initialized")
    
    # ============================================================
    # MAIN REPORT GENERATION
    # ============================================================
    
    def generate_assessment_report(
        self,
        assessment_data: Dict[str, Any],
        format: str = "pdf",
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive assessment report
        
        Args:
            assessment_data: Assessment result with scoring
            format: pdf, json, or csv
            output_path: Optional file path to save report
        
        Returns:
            Report with status and content/path
        """
        if format.lower() not in self.formats:
            return {
                "success": False,
                "error": f"Unsupported format: {format}. Use: {', '.join(self.formats)}"
            }
        
        try:
            if format.lower() == "pdf":
                return self._generate_pdf_report(assessment_data, output_path)
            elif format.lower() == "json":
                return self._generate_json_report(assessment_data, output_path)
            elif format.lower() == "csv":
                return self._generate_csv_report(assessment_data, output_path)
        except Exception as e:
            logger.error(f"Report generation error: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # PDF REPORT GENERATION
    # ============================================================
    
    def _generate_pdf_report(
        self,
        assessment_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate PDF assessment report"""
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_reports/assessment_{timestamp}.pdf"
        
        try:
            # Ensure output directory exists
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch,
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph("Psychological Assessment Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Assessment Summary
            summary_data = [
                ["Assessment Type", assessment_data.get("assessment_name", "Unknown")],
                ["Score", f"{assessment_data.get('total_score', 'N/A')}/{assessment_data.get('max_score', 'N/A')}"],
                ["Percentage", f"{assessment_data.get('percentage', 0):.1f}%"],
                ["Severity Level", assessment_data.get("severity_level", "Unknown").upper()],
                ["Date Completed", assessment_data.get("completed_at", datetime.now().isoformat())],
            ]
            
            summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Interpretation
            story.append(Paragraph("Interpretation", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            interpretation_text = assessment_data.get("interpretation", "No interpretation available")
            story.append(Paragraph(interpretation_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Recommendations
            story.append(Paragraph("Clinical Recommendations", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            recommendations = assessment_data.get("recommendations", [])
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Crisis Resources (if applicable)
            if assessment_data.get("crisis_resources"):
                story.append(PageBreak())
                story.append(Paragraph("Emergency Resources", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                resources = assessment_data.get("crisis_resources", {})
                story.append(Paragraph(f"<b>Crisis Hotline:</b> {resources.get('crisis_line', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"<b>Crisis Text Line:</b> {resources.get('text_line', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"<b>SAMHSA National Helpline:</b> {resources.get('national_helpline', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph("NOTE: If you are in immediate danger, please call 911 or go to the nearest emergency room.", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✅ PDF report generated: {output_path}")
            return {
                "success": True,
                "format": "pdf",
                "path": output_path,
                "message": "PDF report generated successfully"
            }
        
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # JSON REPORT GENERATION
    # ============================================================
    
    def _generate_json_report(
        self,
        assessment_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate JSON assessment report"""
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_reports/assessment_{timestamp}.json"
        
        try:
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            report = {
                "report_type": "assessment",
                "generated_at": datetime.now().isoformat(),
                "assessment": {
                    "type": assessment_data.get("assessment_type"),
                    "name": assessment_data.get("assessment_name"),
                    "score": assessment_data.get("total_score"),
                    "max_score": assessment_data.get("max_score"),
                    "percentage": assessment_data.get("percentage"),
                    "severity_level": assessment_data.get("severity_level"),
                    "interpretation": assessment_data.get("interpretation"),
                    "requires_professional_help": assessment_data.get("requires_professional_help"),
                },
                "recommendations": assessment_data.get("recommendations", []),
                "crisis_resources": assessment_data.get("crisis_resources"),
                "user_id": assessment_data.get("user_id"),
                "session_id": assessment_data.get("session_id"),
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"✅ JSON report generated: {output_path}")
            return {
                "success": True,
                "format": "json",
                "path": output_path,
                "message": "JSON report generated successfully"
            }
        
        except Exception as e:
            logger.error(f"JSON generation error: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # CSV REPORT GENERATION
    # ============================================================
    
    def _generate_csv_report(
        self,
        assessment_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate CSV assessment report"""
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_reports/assessment_{timestamp}.csv"
        
        try:
            import csv
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(["Field", "Value"])
                
                # Assessment data
                writer.writerow(["Assessment Type", assessment_data.get("assessment_type")])
                writer.writerow(["Assessment Name", assessment_data.get("assessment_name")])
                writer.writerow(["Total Score", assessment_data.get("total_score")])
                writer.writerow(["Max Score", assessment_data.get("max_score")])
                writer.writerow(["Percentage", f"{assessment_data.get('percentage', 0):.1f}%"])
                writer.writerow(["Severity Level", assessment_data.get("severity_level")])
                writer.writerow(["Interpretation", assessment_data.get("interpretation")])
                writer.writerow(["Requires Professional Help", assessment_data.get("requires_professional_help")])
                writer.writerow(["Completed At", assessment_data.get("completed_at")])
                
                # Recommendations
                writer.writerow([])
                writer.writerow(["Recommendations"])
                for i, rec in enumerate(assessment_data.get("recommendations", []), 1):
                    writer.writerow([f"  {i}. {rec}"])
                
                # Crisis Resources
                if assessment_data.get("crisis_resources"):
                    writer.writerow([])
                    writer.writerow(["Emergency Resources"])
                    resources = assessment_data.get("crisis_resources", {})
                    for key, value in resources.items():
                        writer.writerow([f"  {key.replace('_', ' ').title()}: {value}"])
            
            logger.info(f"✅ CSV report generated: {output_path}")
            return {
                "success": True,
                "format": "csv",
                "path": output_path,
                "message": "CSV report generated successfully"
            }
        
        except Exception as e:
            logger.error(f"CSV generation error: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # BATCH REPORT GENERATION
    # ============================================================
    
    def generate_batch_reports(
        self,
        assessments: List[Dict[str, Any]],
        formats: List[str] = ["pdf", "json"],
        output_dir: str = "generated_reports"
    ) -> Dict[str, Any]:
        """Generate multiple reports from multiple assessments
        
        Args:
            assessments: List of assessment results
            formats: List of formats to generate
            output_dir: Directory to save reports
        
        Returns:
            Batch report status and file list
        """
        results = {
            "total_assessments": len(assessments),
            "formats_requested": formats,
            "reports_generated": [],
            "failed": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for i, assessment in enumerate(assessments):
            for fmt in formats:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{assessment.get('assessment_type')}_{i}_{timestamp}.{fmt}"
                    output_path = f"{output_dir}/{filename}"
                    
                    result = self.generate_assessment_report(assessment, fmt, output_path)
                    
                    if result.get("success"):
                        results["reports_generated"].append({
                            "assessment_index": i,
                            "assessment_type": assessment.get("assessment_type"),
                            "format": fmt,
                            "path": result.get("path")
                        })
                    else:
                        results["failed"].append({
                            "assessment_index": i,
                            "format": fmt,
                            "error": result.get("error")
                        })
                
                except Exception as e:
                    results["failed"].append({
                        "assessment_index": i,
                        "format": fmt,
                        "error": str(e)
                    })
        
        return results


# Initialize agent
report_agent = ReportGenerationAgent()


if __name__ == "__main__":
    # Test report generation
    sample_assessment = {
        "assessment_type": "phq9",
        "assessment_name": "Patient Health Questionnaire-9 (PHQ-9)",
        "total_score": 15,
        "max_score": 27,
        "percentage": 55.6,
        "severity_level": "moderate",
        "interpretation": "Your score suggests moderate depression symptoms. Professional support is recommended.",
        "recommendations": [
            "Consider scheduling an appointment with a mental health professional",
            "Practice daily exercise and maintain regular sleep schedule",
            "Engage in activities you enjoy",
            "Maintain social connections"
        ],
        "requires_professional_help": True,
        "crisis_resources": {
            "crisis_line": "988",
            "text_line": "Text HOME to 741741",
            "national_helpline": "1-800-662-4357"
        },
        "completed_at": datetime.now().isoformat()
    }
    
    # Generate reports
    for fmt in ["pdf", "json", "csv"]:
        result = report_agent.generate_assessment_report(sample_assessment, fmt)
        print(f"{fmt.upper()}: {result}")
