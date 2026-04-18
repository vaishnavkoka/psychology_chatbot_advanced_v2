"""
Quality Rules - FeatureMate-based semantic quality checks
"""

import re
from typing import List
from unified_linter import Violation, RuleSeverity, UnifiedParser


class QualityRules:
    """FeatureMate-inspired quality rules for semantic validation"""
    
    @staticmethod
    def check_implementation_details(parser: UnifiedParser) -> List[Violation]:
        """FM004: Detect implementation-specific language (clicks, selects, etc)"""
        violations = []
        
        implementation_keywords = [
            r'\bclick(?:s|ed)?\b',
            r'\bselect(?:s|ed)?\b',
            r'\btype(?:s|ed)?\b',
            r'\bscroll(?:s|ed)?\b',
            r'\bpress(?:es|ed)?\b',
            r'\bfill(?:s|ed)?\b',
            r'\benter(?:s|ed)?\b',
            r'\bwait(?:s|ed)?\b',
            r'\brefresh(?:es|ed)?\b',
            r'\bclear(?:s|ed)?\b',
            r'\bfocus(?:es|ed)?\b',
            r'\bhover(?:s|ed)?\b',
            r'\bdouble.click\b',
            r'\bright.click\b',
            r'\bbutton\b',
            r'\blink\b',
            r'\binput\s+field\b',
            r'\btextbox\b',
            r'\bcheckbox\b',
            r'\break\b',
        ]
        
        pattern = '|'.join(implementation_keywords)
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                if re.search(pattern, stripped, re.IGNORECASE):
                    match = re.search(pattern, stripped, re.IGNORECASE)
                    violations.append(Violation(
                        line=i, column=match.start(),
                        rule_id='Q001', rule_name='Implementation detail',
                        severity=RuleSeverity.WARNING,
                        message=f'Implementation detail detected: "{match.group()}"',
                        suggestion='Use business language instead of UI actions',
                        category='quality'
                    ))
        
        return violations
    
    @staticmethod
    def check_vague_language(parser: UnifiedParser) -> List[Violation]:
        """FM005: Detect vague language (basic, simple, some, etc)"""
        violations = []
        
        vague_words = [
            r'\bbasic\b',
            r'\bsimple\b',
            r'\bsome\b',
            r'\bvarious\b',
            r'\bstuff\b',
            r'\bthing(?:s)?\b',
            r'\betc\b',
            r'\band\s+so\s+on\b',
            r'\bmaybe\b',
            r'\bprobably\b',
            r'\bmight\b',
            r'\bcould\b',
            r'\bshould\b',
            r'\bverify\b',
            r'\bcheck\b',
            r'\btest\b',
            r'\bvalidate\b',
            r'\bensure\b',
        ]
        
        pattern = '|'.join(vague_words)
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                if re.search(pattern, stripped, re.IGNORECASE):
                    match = re.search(pattern, stripped, re.IGNORECASE)
                    violations.append(Violation(
                        line=i, column=match.start(),
                        rule_id='Q002', rule_name='Vague language',
                        severity=RuleSeverity.INFO,
                        message=f'Vague term: "{match.group()}"',
                        suggestion='Be more specific about what you mean',
                        category='quality'
                    ))
        
        return violations
    
    @staticmethod
    def check_step_complexity(parser: UnifiedParser) -> List[Violation]:
        """Q003: Check for overly complex scenarios (ideal: 3-7 steps)"""
        violations = []
        in_scenario = False
        step_count = 0
        scenario_line = 0
        scenario_name = ""
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('Scenario'):
                if in_scenario:
                    if step_count < 3:
                        violations.append(Violation(
                            line=scenario_line, column=1,
                            rule_id='Q003', rule_name='Too few steps',
                            severity=RuleSeverity.INFO,
                            message=f'Scenario "{scenario_name}" has only {step_count} steps',
                            suggestion='Consider adding more context or assertions',
                            category='quality'
                        ))
                    elif step_count > 7:
                        violations.append(Violation(
                            line=scenario_line, column=1,
                            rule_id='Q003', rule_name='Too many steps',
                            severity=RuleSeverity.WARNING,
                            message=f'Scenario "{scenario_name}" has {step_count} steps (ideal: 3-7)',
                            suggestion='Break into smaller, focused scenarios',
                            category='quality'
                        ))
                
                in_scenario = True
                step_count = 0
                scenario_line = i
                scenario_name = re.sub(r'^Scenario.*?:\s*', '', stripped)
            
            elif in_scenario and stripped.startswith(('Feature', 'Background')):
                in_scenario = False
            
            if in_scenario and any(stripped.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                step_count += 1
        
        return violations
    
    @staticmethod
    def check_scenario_naming(parser: UnifiedParser) -> List[Violation]:
        """Q004: Check scenario names follow business language"""
        violations = []
        test_keywords = ['test', 'verify', 'check', 'validate', 'should', 'should not']
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if stripped.startswith('Scenario'):
                name = re.sub(r'^Scenario.*?:\s*', '', stripped)
                
                for keyword in test_keywords:
                    if keyword in name.lower():
                        violations.append(Violation(
                            line=i, column=1,
                            rule_id='Q004', rule_name='Test language in scenario',
                            severity=RuleSeverity.INFO,
                            message=f'Scenario uses technical term: "{keyword}"',
                            suggestion='Use business language (what, not how)',
                            category='quality'
                        ))
                        break
                
                # Check if scenario name is too vague
                if len(name) < 10:
                    violations.append(Violation(
                        line=i, column=1,
                        rule_id='Q005', rule_name='Vague scenario name',
                        severity=RuleSeverity.INFO,
                        message=f'Scenario name too generic: "{name}"',
                        suggestion='Use descriptive scenario names',
                        category='quality'
                    ))
        
        return violations
    
    @staticmethod
    def check_mock_data(parser: UnifiedParser) -> List[Violation]:
        """Q006: Detect hardcoded mock data that should be parameterized"""
        violations = []
        
        # Look for common mock values
        mock_patterns = [
            (r'\buser123\b', 'hardcoded user ID'),
            (r'\btest@test\.com\b', 'hardcoded email'),
            (r'\bpassword123\b', 'hardcoded password'),
            (r'\b1234\b', 'hardcoded number'),
            (r'\bjohn.doe\b', 'hardcoded name'),
            (r'\b999-99-9999\b', 'hardcoded SSN'),
        ]
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                for pattern, description in mock_patterns:
                    if re.search(pattern, stripped, re.IGNORECASE):
                        violations.append(Violation(
                            line=i, column=1,
                            rule_id='Q006', rule_name='Mock data',
                            severity=RuleSeverity.INFO,
                            message=f'Step contains {description}',
                            suggestion='Use parameterized test data or Examples tables',
                            category='quality'
                        ))
                        break
        
        return violations
    
    @staticmethod
    def check_negation_clarity(parser: UnifiedParser) -> List[Violation]:
        """Q007: Check for unclear negation (double negatives, etc)"""
        violations = []
        
        negation_patterns = [
            r'should\s+not\s+be\s+unable',
            r'should\s+not\s+fail',
            r'should\s+not\s+be\s+invalid',
            r'is\s+not\s+disabled',
            r'is\s+not\s+hidden',
        ]
        
        pattern = '|'.join(negation_patterns)
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                if re.search(pattern, stripped, re.IGNORECASE):
                    violations.append(Violation(
                        line=i, column=1,
                        rule_id='Q007', rule_name='Unclear negation',
                        severity=RuleSeverity.WARNING,
                        message='Step uses complex negation',
                        suggestion='Rewrite with positive assertions',
                        category='quality'
                    ))
        
        return violations
    
    @staticmethod
    def check_duplicate_scenarios(parser: UnifiedParser) -> List[Violation]:
        """Q008: Detect semantically similar scenarios"""
        violations = []
        scenario_map = {}
        
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            if stripped.startswith('Scenario'):
                name = re.sub(r'^Scenario.*?:\s*', '', stripped).lower()
                
                # Simple similarity check - look for same first few words
                key = ' '.join(name.split()[:3])
                
                if key in scenario_map:
                    first_line = scenario_map[key]
                    violations.append(Violation(
                        line=i, column=1,
                        rule_id='Q008', rule_name='Similar scenarios',
                        severity=RuleSeverity.INFO,
                        message=f'Scenario may be similar to line {first_line}',
                        suggestion='Consider using Scenario Outline for variations',
                        category='quality'
                    ))
                else:
                    scenario_map[key] = i
        
        return violations
    
    @staticmethod
    def check_spelling(parser: UnifiedParser) -> List[Violation]:
        """SY001: Detect spelling errors in feature file"""
        violations = []
        
        # Try to import spell checker
        try:
            from spellchecker import SpellChecker
        except ImportError:
            # If pyspellchecker not installed, skip this check
            return violations
        
        # Create spell checker with custom dictionary
        spell = SpellChecker()
        
        # Add Gherkin and BDD-specific terms to whitelist
        bdd_terms = {
            'feature', 'scenario', 'given', 'when', 'then', 'and', 'but', 'outline',
            'background', 'examples', 'gherkin', 'bdd', 'cucumber', 'pytest', 'behave',
            'automation', 'qa', 'tester', 'login', 'logout', 'password', 'username',
            'api', 'database', 'endpoint', 'payload', 'response', 'request',
            'selenium', 'webdriver', 'xpath', 'css', 'element', 'browser',
            'testng', 'junit', 'fixture', 'assertion', 'validation',
            'scenario', 'scenarios', 'feature', 'features',
            'authenticate', 'authorization', 'verification', 'application',
            'email', 'firstname', 'lastname', 'firstname', 'admin', 'user',
            'data', 'test', 'testing', 'assert', 'verify', 'check',
        }
        spell.word_extractor.word_split_pattern = r'\b[a-z]+(?:_[a-z]+)*\b'
        spell.known_by_language['en'].update(bdd_terms)
        
        # Check Feature, Scenario, and Step lines for spelling
        lines_to_check = []
        for i, line in enumerate(parser.lines, 1):
            stripped = line.strip()
            # Check feature, scenario, and step lines
            if any(stripped.startswith(kw) for kw in ['Feature:', 'Scenario:', 'Scenario Outline:', 'Given', 'When', 'Then', 'And', 'But', 'Background:']):
                lines_to_check.append((i, line))
        
        # Check each line for spelling errors
        for line_num, line in lines_to_check:
            # Extract text (remove gherkin keywords)
            text = re.sub(r'^(Feature:|Scenario:|Scenario Outline:|Given|When|Then|And|But|Background:)\s*', '', line.strip(), flags=re.IGNORECASE)
            
            # Split by spaces, keeping camelCase and snake_case words intact
            words = re.findall(r'\b[a-zA-Z]+(?:_[a-zA-Z]+|\b)', text)
            
            # Check for misspellings
            misspelled = spell.unknown(words)
            
            for word in misspelled:
                # Skip single letters and numbers
                if len(word) <= 1 or word.isdigit():
                    continue
                
                # Get suggestions
                suggestions = spell.correction(word)
                col = line.find(word)
                
                if col >= 0:
                    violations.append(Violation(
                        line=line_num, column=col,
                        rule_id='SY001', rule_name='Spelling error',
                        severity=RuleSeverity.INFO,
                        message=f'Possible spelling error: "{word}"',
                        suggestion=f'Did you mean: "{suggestions}"?' if suggestions else 'Check spelling',
                        category='quality'
                    ))
        
        return violations
