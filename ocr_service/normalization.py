"""
Normalization & Data Cleaning - Medical Documents
"""
import re
from datetime import datetime


class DataNormalizer:
    """Normalize & clean extracted data"""
    
    # Disease synonyms mapping
    DISEASE_SYNONYMS = {
        'demam': 'DEMAM',
        'fever': 'DEMAM',
        'febris': 'DEMAM',
        'panas': 'DEMAM',
        'tipes': 'TIPES',
        'typhoid': 'TIPES',
        'demam tifoid': 'TIPES',
        'pneumonia': 'PNEUMONIA',
        'paru': 'PNEUMONIA',
        'radang paru': 'PNEUMONIA',
        'batuk': 'BATUK',
        'cough': 'BATUK',
        'batuk rejan': 'BATUK',
        'influenza': 'INFLUENZA',
        'flu': 'INFLUENZA',
        'gastritis': 'GASTRITIS',
        'maag': 'GASTRITIS',
        'perut kram': 'GASTRITIS',
        'cedera': 'CEDERA',
        'luka': 'CEDERA',
        'injury': 'CEDERA',
        'trauma': 'CEDERA',
        'fraktur': 'FRAKTUR',
        'patah': 'FRAKTUR',
        'diare': 'DIARE',
        'diarea': 'DIARE',
        'istirahat': 'ISTIRAHAT',
        'rest': 'ISTIRAHAT',
        'operasi': 'OPERASI',
        'surgery': 'OPERASI',
        'bedah': 'OPERASI',
    }
    
    @staticmethod
    def normalize_name(name):
        """Normalize nama - strip dan title case"""
        if not name:
            return None
        
        name = str(name).strip()
        # Remove multiple spaces
        name = re.sub(r'\s+', ' ', name)
        # Title case
        name = name.title()
        
        return name if len(name) > 1 else None
    
    @staticmethod
    def normalize_date(date_str):
        """Normalize tanggal ke format YYYY-MM-DD"""
        if not date_str:
            return None
        
        date_str = str(date_str).strip()
        
        month_map = {
            'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
            'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
            'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12',
        }
        
        # Pattern: "dd bulan yyyy"
        match = re.match(r'(\d{1,2})\s+([a-z]+)\s+(\d{4})', date_str.lower())
        if match:
            day, month_name, year = match.groups()
            month = month_map.get(month_name)
            if month:
                return f"{year}-{month}-{int(day):02d}"
        
        # Pattern: "dd/mm/yyyy"
        match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Pattern: "yyyy-mm-dd"
        match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Pattern: "dd-mm-yyyy"
        match = re.match(r'(\d{1,2})-(\d{1,2})-(\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        return None
    
    @staticmethod
    def normalize_diagnosis(diagnosis_str):
        """Normalize diagnosa ke format standard"""
        if not diagnosis_str:
            return None
        
        diagnosis_lower = str(diagnosis_str).lower().strip()
        # Remove extra spaces
        diagnosis_lower = re.sub(r'\s+', ' ', diagnosis_lower)
        
        # Check direct synonym match
        if diagnosis_lower in DataNormalizer.DISEASE_SYNONYMS:
            return DataNormalizer.DISEASE_SYNONYMS[diagnosis_lower]
        
        # Check partial match (ambil kata pertama atau full match)
        for key, value in DataNormalizer.DISEASE_SYNONYMS.items():
            if key in diagnosis_lower:
                return value
        
        # If not in synonym, return normalized version
        return diagnosis_str.upper().strip()
    
    @staticmethod
    def normalize_cost(cost):
        """Ensure cost adalah integer"""
        if isinstance(cost, int):
            return cost
        
        if isinstance(cost, str):
            # Remove non-numeric characters
            cost_clean = re.sub(r'[^\d]', '', cost)
            try:
                return int(cost_clean) if cost_clean else 0
            except:
                return 0
        
        if isinstance(cost, float):
            return int(cost)
        
        return 0
    
    @staticmethod
    def normalize_nik(nik):
        """Normalize NIK - hapus spasi, pastikan numeric"""
        if not nik:
            return None
        
        nik = str(nik).replace(' ', '').replace('-', '').strip()
        
        if nik.isdigit() and len(nik) >= 10:
            return nik
        
        return None
    
    @staticmethod
    def normalize_invoice_number(inv_num):
        """Normalize nomor invoice"""
        if not inv_num:
            return None
        
        # Keep only alphanumeric and separators
        inv_num = str(inv_num).strip()
        inv_num = re.sub(r'\s+', '', inv_num)  # Remove spaces
        
        return inv_num if len(inv_num) > 2 else None
    
    @staticmethod
    def clean_text(text):
        """Generic text cleaning"""
        if not text:
            return None
        
        text = str(text).strip()
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep common ones
        text = re.sub(r'[^\w\s\-.,()/#&]', '', text, flags=re.UNICODE)
        
        return text if len(text) > 1 else None
    
    @staticmethod
    def normalize_all(data_dict):
        """Normalize semua field dalam dictionary"""
        normalized = {}
        
        for key, value in data_dict.items():
            if key in ['patient_name', 'hospital_name', 'doctor_name']:
                normalized[key] = DataNormalizer.normalize_name(value)
            elif key in ['invoice_date', 'sick_date_from', 'sick_date_to', 'tanggal', 'tanggal_izin']:
                normalized[key] = DataNormalizer.normalize_date(value)
            elif key in ['diagnosis', 'diagnosa']:
                normalized[key] = DataNormalizer.normalize_diagnosis(value)
            elif key in ['total_cost', 'biaya']:
                normalized[key] = DataNormalizer.normalize_cost(value)
            elif key == 'nik':
                normalized[key] = DataNormalizer.normalize_nik(value)
            elif key == 'invoice_number':
                normalized[key] = DataNormalizer.normalize_invoice_number(value)
            else:
                # Default: clean text
                normalized[key] = DataNormalizer.clean_text(value) if value else None
        
        return normalized
