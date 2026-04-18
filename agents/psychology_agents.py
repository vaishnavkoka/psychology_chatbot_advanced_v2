"""
Assessment Agent for Psychology Chatbot
Conducts psychological assessments and evaluations
"""

import json
import os
from typing import Dict, List, Any
from groq import Groq

class AssessmentAgent:
    """Conducts psychological assessments"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.assessments = self._load_assessments()
    
    def _load_assessments(self) -> Dict:
        """Load assessment data"""
        try:
            with open("data/psychology_db/assessments.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"assessments": []}
    
    def get_available_assessments(self) -> List[Dict]:
        """Get list of available assessments"""
        return [
            {
                "id": a["id"],
                "name": a["name"],
                "type": a["type"],
                "questions_count": len(a["questions"])
            }
            for a in self.assessments.get("assessments", [])
        ]
    
    def conduct_assessment(self, assessment_id: str, responses: List[int]) -> Dict[str, Any]:
        """Conduct assessment and generate results"""
        assessment = next(
            (a for a in self.assessments.get("assessments", []) if a["id"] == assessment_id),
            None
        )
        
        if not assessment:
            return {"error": "Assessment not found"}
        
        if len(responses) != len(assessment["questions"]):
            return {"error": "Invalid number of responses"}
        
        # Calculate score
        total_score = sum(responses)
        
        # Get interpretation
        scoring = assessment.get("scoring", {})
        interpretation = "No scoring available"
        
        for range_str, result in scoring.items():
            parts = range_str.split("-")
            min_score = int(parts[0])
            max_score = int(parts[1])
            if min_score <= total_score <= max_score:
                interpretation = result
                break
        
        return {
            "assessment": assessment["name"],
            "total_score": total_score,
            "interpretation": interpretation,
            "recommendations": self._generate_recommendations(assessment["type"], total_score)
        }
    
    def _generate_recommendations(self, assessment_type: str, score: int) -> List[str]:
        """Generate recommendations based on assessment"""
        recommendations = []
        
        if assessment_type == "depression_screening" and score >= 15:
            recommendations.extend([
                "Consider reaching out to a mental health professional",
                "Practice physical activity - even 20 minutes daily helps",
                "Maintain social connections",
                "Consider therapy or counseling"
            ])
        elif assessment_type == "anxiety_assessment" and score >= 10:
            recommendations.extend([
                "Practice breathing exercises daily",
                "Limit caffeine intake",
                "Try meditation or mindfulness",
                "Consider professional support"
            ])
        
        return recommendations
    
    def get_assessment_details(self, assessment_id: str) -> Dict[str, Any]:
        """Get detailed assessment information"""
        assessment = next(
            (a for a in self.assessments.get("assessments", []) if a["id"] == assessment_id),
            None
        )
        return assessment if assessment else {"error": "Assessment not found"}
    
    def analyze_score_with_ai(self, assessment_type: str, score: int, context: str = "") -> str:
        """Use AI to provide detailed analysis of assessment results"""
        prompt = f"""
You are a compassionate psychology assistant. Analyze this assessment result:
- Assessment Type: {assessment_type}
- Score: {score}
- Context: {context if context else 'No additional context provided'}

Provide:
1. What this score typically indicates
2. Specific recommendations
3. Encouraging message
4. When to seek professional help

Keep response supportive and non-clinical. Maximum 300 words.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return message.choices[0].message.content
        except Exception as e:
            return f"Unable to generate analysis: {str(e)}"

class SupportAgent:
    """Provides emotional support and coping strategies"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"  # More powerful for therapeutic responses
        self.coping_strategies = self._load_coping_strategies()
    
    def _load_coping_strategies(self) -> Dict:
        """Load coping strategies data"""
        try:
            with open("data/psychology_db/coping_strategies.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"coping_strategies": []}
    
    def provide_support(self, user_message: str, context: Dict = None) -> str:
        """Provide emotional support and guidance"""
        prompt = f"""
You are a highly empathetic and supportive psychology assistant. The user has shared:
"{user_message}"

Context: {json.dumps(context) if context else 'No context provided'}

Respond with:
1. Validation of their feelings
2. Gentle encouragement
3. Practical suggestions (if appropriate)
4. Offer of additional support

Important: Be warm, non-judgmental, and supportive. This is NOT professional therapy.
If they express suicidal thoughts, provide crisis resources.
Keep response to 200-300 words.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.8
            )
            return message.choices[0].message.content
        except Exception as e:
            return f"I'm here to listen and support you. Could you tell me more about what you're experiencing?"
    
    def get_coping_strategies(self, issue: str, category: str = None) -> List[Dict]:
        """Get coping strategies for specific issue"""
        strategies = self.coping_strategies.get("coping_strategies", [])
        
        if category:
            strategies = [s for s in strategies if s.get("category") == category]
        
        return strategies[:5]  # Return top 5 strategies
    
    def recommend_exercise(self, mood: int, time_available: int = 30) -> Dict:
        """Recommend mindfulness or coping exercise based on mood"""
        mindfulness_data = self._load_mindfulness()
        exercises = mindfulness_data.get("mindfulness_exercises", [])
        
        # Filter by difficulty and duration
        suitable = [
            e for e in exercises
            if int(e["duration"].split("-")[0]) <= time_available
        ]
        
        if mood <= 2:
            suitable = [e for e in suitable if e["difficulty"] == "beginner"]
        
        if suitable:
            return suitable[0]
        return exercises[0] if exercises else {}
    
    def _load_mindfulness(self) -> Dict:
        """Load mindfulness exercises"""
        try:
            with open("data/psychology_db/mindfulness_exercises.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"mindfulness_exercises": []}

class InsightAgent:
    """Provides psychological insights and understanding"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"  # Long context for detailed insights
        self.mental_health_topics = self._load_topics()
    
    def _load_topics(self) -> Dict:
        """Load mental health topics"""
        try:
            with open("data/psychology_db/mental_health_topics.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"mental_health_topics": []}
    
    def get_topic_info(self, topic: str) -> Dict:
        """Get information about mental health topic"""
        topics = self.mental_health_topics.get("mental_health_topics", [])
        return next((t for t in topics if t["topic"].lower() == topic.lower()), None)
    
    def provide_insight(self, query: str) -> str:
        """Provide psychological insight on query"""
        prompt = f"""
You are a knowledgeable psychology educator. The user asks:
"{query}"

Provide:
1. Clear explanation
2. Psychological background
3. Practical applications
4. Scientific validation (if applicable)

Keep response informative but accessible. Maximum 300 words.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return message.choices[0].message.content
        except Exception as e:
            return "Unable to generate insight at this time"
    
    def explain_concept(self, concept: str) -> str:
        """Explain psychological concept"""
        prompt = f"""
Explain the psychological concept of "{concept}" in simple terms:
1. Definition
2. Why it matters
3. Example from daily life
4. How it relates to well-being

Keep it clear and relatable. Do not exceed 250 words.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return message.choices[0].message.content
        except Exception as e:
            return "Unable to explain concept"

class RecommendationAgent:
    """Recommends techniques and resources"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.cbt_techniques = self._load_cbt()
    
    def _load_cbt(self) -> Dict:
        """Load CBT techniques"""
        try:
            with open("data/psychology_db/cbt_techniques.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"cbt_techniques": []}
    
    def recommend_cbt_technique(self, issue: str) -> Dict:
        """Recommend CBT technique for specific issue"""
        techniques = self.cbt_techniques.get("cbt_techniques", [])
        
        # Simple matching based on issue keywords
        issue_lower = issue.lower()
        recommended = []
        
        for technique in techniques:
            if any(word in technique["description"].lower() for word in issue_lower.split()):
                recommended.append(technique)
        
        return recommended[0] if recommended else techniques[0]
    
    def personalize_recommendations(self, profile: Dict) -> List[str]:
        """Generate personalized recommendations based on user profile"""
        recommendations = []
        
        if profile.get("depression_score", 0) > 10:
            recommendations.append("Regular physical activity (30 min daily)")
            recommendations.append("Behavioral activation - schedule enjoyable activities")
        
        if profile.get("anxiety_score", 0) > 10:
            recommendations.append("Daily breathing exercises (5-10 minutes)")
            recommendations.append("Exposure to feared situations gradually")
        
        if profile.get("sleep_quality", 5) < 3:
            recommendations.append("Improve sleep hygiene - consistent schedule")
            recommendations.append("No screens 1 hour before bed")
        
        if not recommendations:
            recommendations = [
                "Daily mindfulness meditation",
                "Regular physical activity",
                "Maintain social connections"
            ]
        
        return recommendations
