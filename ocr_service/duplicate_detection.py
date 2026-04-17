"""
Duplicate Detection - Detect potential duplicate submissions
"""


class DuplicateDetector:
    """Detect potential duplicate medical submissions"""
    
    def __init__(self):
        # Scoring weights (total 100%)
        self.weights = {
            'invoice_number': 60,  # Invoice number match is strongest indicator
            'patient_name': 20,
            'hospital_name': 10,
            'total_cost': 10,
        }
    
    def calculate_similarity(self, new_submission, existing_submissions):
        """
        Calculate duplicate score between new and existing submissions
        
        Returns: (is_duplicate: bool, highest_score: float, details: dict)
        """
        if not existing_submissions:
            return False, 0.0, {}
        
        highest_score = 0.0
        similar_records = []
        
        for existing in existing_submissions:
            score = 0.0
            matches = []
            
            # Check invoice number (bobot 60%) - strongest indicator
            new_inv = str(new_submission.get('invoice_number', '')).strip()
            existing_inv = str(existing.get('invoice_number', '')).strip()
            
            if new_inv and existing_inv and new_inv == existing_inv:
                score += self.weights['invoice_number']
                matches.append('Nomor Kwitansi sama')
            
            # Check patient name (bobot 20%)
            new_patient = str(new_submission.get('patient_name', '')).lower().strip()
            existing_patient = str(existing.get('patient_name', '')).lower().strip()
            
            if new_patient and existing_patient and new_patient == existing_patient:
                score += self.weights['patient_name']
                matches.append('Nama Pasien sama')
            
            # Check hospital name (bobot 10%)
            new_hospital = str(new_submission.get('hospital_name', '')).lower().strip()
            existing_hospital = str(existing.get('hospital_name', '')).lower().strip()
            
            if new_hospital and existing_hospital and new_hospital == existing_hospital:
                score += self.weights['hospital_name']
                matches.append('Rumah Sakit sama')
            
            # Check total cost (bobot 10%)
            new_cost = int(new_submission.get('total_cost') or 0)
            existing_cost = int(existing.get('total_cost') or 0)
            
            if new_cost > 0 and existing_cost > 0 and new_cost == existing_cost:
                score += self.weights['total_cost']
                matches.append('Total Biaya sama')
            
            # Threshold: 70% = flag duplicate
            if score >= 70:
                highest_score = max(highest_score, score)
                similar_records.append({
                    'score': score,
                    'matches': matches,
                    'submission_id': existing.get('submission_id'),
                })
        
        if highest_score >= 70:
            # Build detail message
            all_matches = []
            submission_ids = []
            for sr in similar_records:
                all_matches.extend(sr['matches'])
                submission_ids.append(sr['submission_id'])
            
            details = {
                'is_duplicate': True,
                'score': highest_score,
                'matches': list(set(all_matches)),  # Remove duplicates
                'similar_submission_ids': submission_ids,
                'warning': f"⚠️ POTENSI DUPLIKAT ({highest_score}%): {' & '.join(list(set(all_matches)))}",
            }
            
            return True, highest_score, details
        
        return False, highest_score, {
            'is_duplicate': False,
            'score': highest_score,
            'matches': [],
            'similar_submission_ids': [],
            'warning': None,
        }
    
    def check_duplicate(self, new_submission, existing_submissions):
        """
        Convenience method - returns just the bool
        """
        is_dup, score, details = self.calculate_similarity(new_submission, existing_submissions)
        return is_dup
    
    def get_duplicate_warning(self, is_duplicate, score, matches):
        """Generate warning message"""
        if not is_duplicate:
            return None
        
        note = " & ".join(matches) if matches else "Multiple matches"
        return f"⚠️ POTENSI DUPLIKAT ({score}%): {note}"
