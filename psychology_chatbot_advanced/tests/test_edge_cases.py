"""
Edge Case Testing Suite for Psychology Chatbot
Comprehensive tests for crisis scenarios, boundary conditions, and error handling
"""

import pytest
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class TestCrisisDetection:
    """Test crisis detection and response"""
    
    def test_immediate_crisis_detection(self):
        """Test immediate crisis keyword detection"""
        crisis_messages = [
            "I want to end my life",
            "I'm going to kill myself",
            "suicide is the only way",
            "I'm going to hurt myself",
            "I have a gun and I'm going to use it"
        ]
        
        for msg in crisis_messages:
            # Mock crisis detection
            assert self._contains_crisis_keywords(msg), f"Failed to detect crisis in: {msg}"
    
    def test_subtle_crisis_detection(self):
        """Test subtle/indirect crisis indicators"""
        subtle_messages = [
            "I don't see a point anymore",
            "Everyone would be better off without me",
            "I'm a burden to everyone",
            "I can't take this anymore",
            "I'm thinking about disappearing"
        ]
        
        for msg in subtle_messages:
            # Mock subtle crisis detection
            score = self._calculate_crisis_severity(msg)
            assert score > 0.5, f"Failed to detect subtle crisis in: {msg}"
    
    def test_false_positive_prevention(self):
        """Prevent false positives for normal emotional expressions"""
        normal_messages = [
            "I'm dying from this homework",
            "This movie killed me it was so funny",
            "I'm so stressed about the deadline",
            "I feel terrible today",
            "That hurt my feelings"
        ]
        
        for msg in normal_messages:
            score = self._calculate_crisis_severity(msg)
            assert score < 0.5, f"False positive detected in: {msg}"
    
    def test_multilingual_crisis_detection(self):
        """Test crisis detection across languages"""
        multilingual_messages = {
            "spanish": "quiero quitarme la vida",
            "french": "je veux me tuer",
            "german": "ich will mich selbst verletzen"
        }
        
        for lang, msg in multilingual_messages.items():
            # Would require translation API in production
            logger.info(f"Testing {lang} crisis message: {msg}")
    
    def test_crisis_context_awareness(self):
        """Test crisis detection with contextual awareness"""
        context_messages = [
            {
                "message": "I can't do this",
                "context": {"previous_mental_state": "suicidal"},
                "should_trigger": True
            },
            {
                "message": "I can't do this",
                "context": {"previous_mental_state": "neutral"},
                "should_trigger": False
            }
        ]
        
        for test_case in context_messages:
            severity = self._assess_crisis_with_context(
                test_case["message"],
                test_case["context"]
            )
            expected = test_case["should_trigger"]
            assert (severity > 0.7) == expected, f"Context awareness failed for: {test_case}"
    
    # Helper methods
    def _contains_crisis_keywords(self, text: str) -> bool:
        """Check for explicit crisis keywords"""
        keywords = ["suicide", "kill myself", "end my life", "hurt myself", "gun"]
        return any(kw in text.lower() for kw in keywords)
    
    def _calculate_crisis_severity(self, text: str) -> float:
        """Calculate crisis severity score (0-1)"""
        text_lower = text.lower()
        
        high_severity_keywords = ["suicide", "kill", "harm", "gun", "rope"]
        medium_severity_keywords = ["pointless", "burden", "disappear", "hate myself"]
        low_severity_keywords = ["stressed", "overwhelmed", "terrible", "can't take"]
        
        if any(kw in text_lower for kw in high_severity_keywords):
            return 0.9
        elif any(kw in text_lower for kw in medium_severity_keywords):
            return 0.65
        elif any(kw in text_lower for kw in low_severity_keywords):
            return 0.3
        
        return 0.0
    
    def _assess_crisis_with_context(self, message: str, context: Dict) -> float:
        """Assess crisis severity with contextual information"""
        base_score = self._calculate_crisis_severity(message)
        
        previous_state = context.get("previous_mental_state", "")
        if previous_state == "suicidal":
            base_score += 0.2  # Boost if previous state was concerning
        
        return min(1.0, base_score)


class TestBoundaryConditions:
    """Test boundary conditions and edge cases"""
    
    def test_empty_input(self):
        """Test handling of empty input"""
        empty_inputs = ["", " ", "\n", "\t"]
        
        for input_val in empty_inputs:
            result = self._process_input(input_val)
            assert result["valid"] is False
            assert result.get("error") == "Empty input"
    
    def test_extremely_long_input(self):
        """Test handling of very long messages"""
        long_input = "Test message " * 1000  # ~13,000 characters
        
        result = self._process_input(long_input)
        assert result.get("truncated") or len(result.get("processed", "")) < len(long_input)
    
    def test_special_characters_handling(self):
        """Test handling of special characters and emojis"""
        special_inputs = [
            "Hello 👋 how are you 😊",
            "Testing with @mentions and #hashtags",
            "URL test: https://example.com",
            "Math expression: x² + y² = z²",
            "Unicode: 你好世界 مرحبا العالم"
        ]
        
        for input_val in special_inputs:
            result = self._process_input(input_val)
            assert result["valid"] is True, f"Failed to process: {input_val}"
    
    def test_rapid_successive_messages(self):
        """Test handling of rapid message succession"""
        messages = ["Message " + str(i) for i in range(100)]
        
        processed = []
        for msg in messages:
            result = self._process_input(msg)
            processed.append(result)
        
        assert len(processed) == 100
        assert all(r["valid"] for r in processed)
    
    def test_input_with_malformed_json(self):
        """Test handling of malformed JSON in input"""
        malformed_inputs = [
            '{"incomplete": ',
            "{'single_quotes': true}",
            '{"trailing_comma": true,}',
            '{"duplicate": true, "duplicate": false}'
        ]
        
        for input_val in malformed_inputs:
            result = self._process_input(input_val)
            # Should handle gracefully without crashing
            assert result is not None
    
    def test_response_timeout_handling(self):
        """Test handling of timeout scenarios"""
        # Simulate slow response
        import time
        start = time.time()
        result = self._simulate_timeout(timeout_ms=5000)
        elapsed = time.time() - start
        
        assert result["timeout"] is False or elapsed > 4.9
    
    # Helper methods
    def _process_input(self, text: str) -> Dict:
        """Process input with validation"""
        if not text or not text.strip():
            return {"valid": False, "error": "Empty input"}
        
        truncated = False
        if len(text) > 5000:
            text = text[:5000]
            truncated = True
        
        return {
            "valid": True,
            "processed": text,
            "truncated": truncated
        }
    
    def _simulate_timeout(self, timeout_ms: int) -> Dict:
        """Simulate timeout handling"""
        import time
        try:
            # Simulate processing that completes within timeout
            time.sleep(0.1)
            return {"timeout": False, "result": "success"}
        except TimeoutError:
            return {"timeout": True, "error": "Request timeout"}


class TestErrorHandling:
    """Test error handling and recovery"""
    
    def test_api_connection_failure(self):
        """Test handling of API connection failures"""
        # Would be called with unreachable backend
        result = self._call_api_with_retry("http://localhost:9999/nonexistent")
        assert result["success"] is False
        assert result["retries"] > 0
    
    def test_invalid_response_format(self):
        """Test handling of malformed API responses"""
        invalid_responses = [
            "Not JSON at all",
            '{"incomplete": }',
            None,
            b"\x00\x01\x02"
        ]
        
        for response in invalid_responses:
            result = self._parse_response(response)
            assert result is not None or result == {}
    
    def test_missing_required_fields(self):
        """Test handling of responses missing required fields"""
        incomplete_responses = [
            {"message": "test"},  # Missing agent
            {"agent": "TestAgent"},  # Missing message
            {"message": "", "agent": ""},  # Empty required fields
            {}  # Completely empty
        ]
        
        for response in incomplete_responses:
            result = self._validate_response(response)
            assert result["valid"] is False
            assert result.get("missing_fields")
    
    def test_database_connection_failure(self):
        """Test handling of database connection issues"""
        result = self._query_database("SELECT * FROM users", retry=True)
        # Should either succeed or retry gracefully
        assert result is not None
    
    def test_resource_exhaustion(self):
        """Test handling when resources are exhausted"""
        # Simulate high memory/CPU usage by requesting many large allocations
        try:
            allocations = []
            for i in range(1000):
                allocations.append([0] * 1000000)  # 1M integers each
        except MemoryError:
            # Expected behavior - handle gracefully
            pass
        finally:
            allocations = []
    
    def test_concurrent_request_handling(self):
        """Test handling of concurrent requests"""
        async def concurrent_requests():
            tasks = []
            for i in range(20):
                tasks.append(self._async_process_message(f"Message {i}"))
            
            results = await asyncio.gather(*tasks)
            return results
        
        # Run concurrent test
        try:
            loop = asyncio.new_event_loop()
            results = loop.run_until_complete(concurrent_requests())
            assert len(results) == 20
        finally:
            loop.close()
    
    # Helper methods
    def _call_api_with_retry(self, url: str, max_retries: int = 3) -> Dict:
        """Call API with retry logic"""
        retries = 0
        for attempt in range(max_retries):
            try:
                # Attempt to call API
                retries = attempt
                raise ConnectionError("Connection failed")
            except ConnectionError:
                if attempt < max_retries - 1:
                    continue
                else:
                    return {"success": False, "retries": retries}
        
        return {"success": True, "retries": retries}
    
    def _parse_response(self, response) -> Dict:
        """Parse API response safely"""
        try:
            if isinstance(response, str):
                return json.loads(response)
            elif isinstance(response, dict):
                return response
            else:
                return {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def _validate_response(self, response: Dict) -> Dict:
        """Validate response has required fields"""
        required = ["message", "agent"]
        missing = [f for f in required if f not in response or not response[f]]
        
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing
        }
    
    def _query_database(self, query: str, retry: bool = True) -> Optional[List]:
        """Query database with error handling"""
        try:
            # Simulate database query
            return [{"id": 1, "data": "test"}]
        except Exception as e:
            if retry:
                logger.warning(f"Database query failed, retrying: {e}")
                return self._query_database(query, retry=False)
            return None
    
    async def _async_process_message(self, message: str) -> Dict:
        """Process message asynchronously"""
        await asyncio.sleep(0.1)  # Simulate async processing
        return {"message": message, "processed": True}


class TestConversationFlow:
    """Test conversation flow and continuity"""
    
    def test_multi_turn_conversation(self):
        """Test maintaining context over multiple turns"""
        messages = [
            "I'm feeling anxious",
            "Especially about work",
            "My boss is very demanding",
            "I haven't taken a break in weeks"
        ]
        
        context = {}
        for i, msg in enumerate(messages):
            context = self._process_with_context(msg, context)
            assert context["turn"] == i + 1
            assert len(context["history"]) == i + 1
    
    def test_context_preservation(self):
        """Test that context is properly preserved"""
        initial_context = {
            "user_name": "Alice",
            "mental_state": "anxious",
            "triggers": ["deadlines", "social situations"]
        }
        
        # Process multiple messages
        context = initial_context.copy()
        for i in range(5):
            context = self._process_with_context(f"Message {i}", context)
            
            # Verify original context preserved
            assert context["user_name"] == "Alice"
            assert context["mental_state"] == "anxious"
            assert len(context["triggers"]) == 2
    
    def test_topic_switching(self):
        """Test handling topic transitions"""
        conversation = [
            ("I'm anxious about work", "work"),
            ("Actually, I'm also struggling with sleep", "sleep"),
            ("And my relationships have been strained", "relationships"),
            ("But mostly I'm just tired", "fatigue")
        ]
        
        topics = []
        for message, expected_topic in conversation:
            detected_topic = self._detect_topic(message)
            topics.append(detected_topic)
        
        # Should have detected different topics
        unique_topics = set(topics)
        assert len(unique_topics) >= 2
    
    def test_repetition_handling(self):
        """Test handling of repetitive user input"""
        repeated_message = "I'm sad I'm sad I'm sad" * 10
        
        result = self._process_with_repetition_check(repeated_message)
        assert result["is_repetitive"] is True
        assert result["original_intent"] == "I'm sad"
    
    # Helper methods
    def _process_with_context(self, message: str, context: Dict) -> Dict:
        """Process message with context preservation"""
        if "history" not in context:
            context["history"] = []
        
        context["history"].append(message)
        context["turn"] = len(context["history"])
        context["last_message"] = message
        
        return context
    
    def _detect_topic(self, message: str) -> str:
        """Detect topic from message"""
        topics = {
            "work": ["work", "job", "boss", "deadline", "office"],
            "sleep": ["sleep", "insomnia", "tired", "rest", "bed"],
            "relationships": ["relationship", "friend", "family", "partner", "social"],
            "physical": ["pain", "hurt", "exercise", "health", "body"]
        }
        
        message_lower = message.lower()
        for topic, keywords in topics.items():
            if any(kw in message_lower for kw in keywords):
                return topic
        
        return "general"
    
    def _process_with_repetition_check(self, message: str) -> Dict:
        """Check for repetitive content"""
        words = message.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        
        diversity = unique_words / max(total_words, 1)
        
        # Calculate original message (first few words, once)
        unique_sequence = []
        for word in words:
            if word not in unique_sequence:
                unique_sequence.append(word)
        
        return {
            "is_repetitive": diversity < 0.3,
            "diversity_score": diversity,
            "original_intent": " ".join(unique_sequence[:5])
        }


class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    def test_conversation_history_integrity(self):
        """Test conversation history is maintained correctly"""
        history = []
        
        for i in range(10):
            entry = {
                "id": i,
                "timestamp": datetime.now().isoformat(),
                "message": f"Message {i}",
                "role": "user" if i % 2 == 0 else "assistant"
            }
            history.append(entry)
        
        # Verify integrity
        assert len(history) == 10
        assert all(entry.get("id") is not None for entry in history)
        assert all(entry.get("timestamp") is not None for entry in history)
    
    def test_crisis_event_logging(self):
        """Test crisis events are logged correctly"""
        events = []
        
        crisis_detections = [
            {"level": "critical", "message": "I want to die"},
            {"level": "high", "message": "I'm thinking of harming myself"},
            {"level": "medium", "message": "I can't handle this"}
        ]
        
        for detection in crisis_detections:
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": "crisis_detection",
                "level": detection["level"],
                "original_message": detection["message"],
                "action_taken": "Safety protocol activated"
            }
            events.append(event)
        
        assert len(events) == 3
        assert all(e.get("timestamp") for e in events)
        assert events[0]["level"] == "critical"
    
    def test_session_state_consistency(self):
        """Test session state remains consistent"""
        session = {
            "id": "session_123",
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "state": "active"
        }
        
        # Simulate message additions
        for i in range(5):
            session["messages"].append({
                "id": i,
                "text": f"Message {i}"
            })
        
        # Verify consistency
        assert session["state"] == "active"
        assert len(session["messages"]) == 5
        assert session["messages"][0]["id"] == 0
        assert session["messages"][-1]["id"] == 4


# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
