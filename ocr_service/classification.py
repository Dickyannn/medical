"""
Disease Classification & Categorization
"""


class DiseaseClassifier:
    """Classify disease dan determine category"""
    
    # Disease master data - expanded untuk dokumen medis
    DISEASE_MASTER = {
        'DEMAM': {
            'code': 'P001',
            'name': 'Demam',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'TIPES': {
            'code': 'P002',
            'name': 'Tipes / Demam Tifoid',
            'category': 'Sedang',
            'reimburseable': True,
        },
        'PNEUMONIA': {
            'code': 'P003',
            'name': 'Pneumonia / Radang Paru',
            'category': 'Berat',
            'reimburseable': True,
        },
        'BATUK': {
            'code': 'P004',
            'name': 'Batuk / Batuk Rejan',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'INFLUENZA': {
            'code': 'P005',
            'name': 'Influenza / Flu',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'GASTRITIS': {
            'code': 'P006',
            'name': 'Gastritis / Maag',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'CEDERA': {
            'code': 'P007',
            'name': 'Cedera / Luka / Trauma',
            'category': 'Sedang',
            'reimburseable': True,
        },
        'FRAKTUR': {
            'code': 'P008',
            'name': 'Fraktur / Patah Tulang',
            'category': 'Berat',
            'reimburseable': True,
        },
        'DIARE': {
            'code': 'P009',
            'name': 'Diare',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'OPERASI': {
            'code': 'P010',
            'name': 'Operasi / Bedah / Surgery',
            'category': 'Berat',
            'reimburseable': True,
        },
        'ISTIRAHAT': {
            'code': 'P011',
            'name': 'Istirahat / Rest',
            'category': 'Ringan',
            'reimburseable': False,
        },
        'PENYAKIT INFEKSI': {
            'code': 'P012',
            'name': 'Penyakit Infeksi',
            'category': 'Sedang',
            'reimburseable': True,
        },
        'PENYAKIT KRONIS': {
            'code': 'P013',
            'name': 'Penyakit Kronis',
            'category': 'Berat',
            'reimburseable': True,
        },
    }
    
    @staticmethod
    def classify(diagnosis):
        """
        Classify diagnosis berdasarkan master data
        
        Returns:
        {
            'disease_code': 'P001',
            'disease_name': 'Demam',
            'category': 'Ringan',
            'reimburseable': False,
            'found': True,
            'warning': None
        }
        """
        if not diagnosis:
            return {
                'disease_code': None,
                'disease_name': diagnosis,
                'category': None,
                'reimburseable': None,
                'found': False,
                'warning': 'Data diagnosa tidak ditemukan',
            }
        
        diagnosis_upper = str(diagnosis).upper().strip()
        
        # Direct match
        if diagnosis_upper in DiseaseClassifier.DISEASE_MASTER:
            info = DiseaseClassifier.DISEASE_MASTER[diagnosis_upper]
            return {
                'disease_code': info['code'],
                'disease_name': info['name'],
                'category': info['category'],
                'reimburseable': info['reimburseable'],
                'found': True,
                'warning': None if info['reimburseable'] else '⚠️ Penyakit tidak dapat direimburse',
            }
        
        # Partial match - check if diagnosis contains any keyword
        for key, info in DiseaseClassifier.DISEASE_MASTER.items():
            if key in diagnosis_upper or diagnosis_upper in key:
                return {
                    'disease_code': info['code'],
                    'disease_name': info['name'],
                    'category': info['category'],
                    'reimburseable': info['reimburseable'],
                    'found': True,
                    'warning': None if info['reimburseable'] else '⚠️ Penyakit tidak dapat direimburse',
                }
        
        # Not found in master
        return {
            'disease_code': None,
            'disease_name': diagnosis,
            'category': None,
            'reimburseable': None,
            'found': False,
            'warning': '⚠️ Diagnosa belum ada di master data - perlu review manual',
        }
    
    @staticmethod
    def get_category(diagnosis):
        """Get kategori dari diagnosis"""
        result = DiseaseClassifier.classify(diagnosis)
        return result['category']
    
    @staticmethod
    def is_reimburseable(diagnosis):
        """Check apakah diagnosis dapat direimburse"""
        result = DiseaseClassifier.classify(diagnosis)
        return result['reimburseable']
    
    @staticmethod
    def get_master_data():
        """Return master data untuk reference"""
        return DiseaseClassifier.DISEASE_MASTER
    
    @staticmethod
    def auto_categorize(diagnosis):
        """
        Auto-categorize diagnosis berdasarkan keywords
        Fallback jika tidak ada di master data
        """
        if not diagnosis:
            return 'Lainnya'
        
        diagnosis_lower = str(diagnosis).lower()
        
        # Category mapping based on keywords
        categories = {
            'Penyakit Infeksi': [
                'infeksi', 'demam', 'tifoid', 'flu', 'pilek', 'batuk',
                'bronkitis', 'pneumonia', 'hepatitis', 'tb', 'tbc',
                'diare', 'malaria', 'istirahat'
            ],
            'Penyakit Kronis': [
                'diabetes', 'hipertensi', 'asma', 'jantung', 'ginjal',
                'kanker', 'stroke', 'kolesterol', 'tekanan darah', 'darah tinggi'
            ],
            'Kecelakaan': [
                'luka', 'patah', 'fraktur', 'trauma', 'cedera', 'benturan',
                'jatuh', 'terkilir', 'memar', 'injury'
            ],
            'Operasi': [
                'operasi', 'pembedahan', 'bedah', 'surgery', 'pasca operasi',
                'post operasi', 'surgical'
            ],
            'Perawatan Gigi': [
                'gigi', 'dental', 'karies', 'pencabutan', 'orthodonti'
            ],
            'Mata': [
                'mata', 'katarak', 'minus', 'buta', 'glaukoma', 'oftalmologi'
            ],
            'THT': [
                'telinga', 'hidung', 'tenggorokan', 'tht', 'otolaringologi',
                'sinusitis', 'otitis', 'faringitis'
            ],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in diagnosis_lower:
                    return category
        
        return 'Lainnya'
    
    @staticmethod
    def _calculate_extraction_confidence(extracted_fields):
        """Calculate confidence score based on field extraction success"""
        if not extracted_fields:
            return 0
        
        doc_type = extracted_fields.get('type', 'kwitansi')
        extracted_count = 0
        total_fields = 0
        
        if doc_type == 'kwitansi':
            fields_to_check = ['hospital_name', 'invoice_number', 'invoice_date', 'total_cost', 'patient_name']
            total_fields = len([f for f in fields_to_check if f in extracted_fields])
            for field in fields_to_check:
                if extracted_fields.get(field):
                    extracted_count += 1
        elif doc_type == 'surat':
            fields_to_check = ['doctor_name', 'diagnosis', 'sick_date_from', 'sick_date_to']
            total_fields = len([f for f in fields_to_check if f in extracted_fields])
            for field in fields_to_check:
                if extracted_fields.get(field):
                    extracted_count += 1
        
        # Calculate percentage
        if total_fields > 0:
            confidence = int((extracted_count / total_fields) * 100)
            return min(confidence, 95)  # Cap at 95%
        
        return 0
