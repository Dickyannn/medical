"""
Enhanced Data Extraction - Adapted for Medical Invoices & Letters
Extraction untuk Kwitansi & Surat Keterangan Sakit
"""
import re
from datetime import datetime


class MedicalDataExtractor:
    """Extract structured data dari OCR text untuk dokumen medis"""
    
    def __init__(self):
        # Indonesian month mapping
        self.month_map = {
            'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
            'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
            'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12',
        }
        
        # NIK pattern
        self.nik_pattern = r'\b(\d{16})\b|\bNIK[:\s]+(\d+)\b'
        
        # Date patterns
        self.date_patterns = [
            r'(\d{1,2})\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember|january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
        ]
    
    # ============================================================
    # KWITANSI / INVOICE EXTRACTION
    # ============================================================
    
    def extract_hospital_name(self, text):
        """Extract nama rumah sakit/klinik"""
        patterns = [
            r'(?:RUMAH SAKIT|RS|KLINIK|CLINIC|HOSPITAL)\s+([A-Z][A-Za-z\s&\.]+?)(?:\n|$)',
            r'^([A-Z][A-Za-z\s&\.]+?)\s*(?:RUMAH SAKIT|RS|KLINIK).*?$',
            r'RUMAH SAKIT\s+(.+?)(?:\nJL|JALAN|JL\.)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                name = re.sub(r'\s+', ' ', name)
                if len(name) > 3:
                    return name[:100]
        
        return None
    
    def extract_invoice_number(self, text):
        """Extract nomor kwitansi/invoice"""
        patterns = [
            r'(?:NOMOR|NO|NUMBER|INV|INVOICE|KWITANSI|RECEIPT)\s*[:\.]?\s*([A-Z0-9\/\-\.\s]+?)(?:\n|$)',
            r'(?:No\.|NUMBER|NO)\s+([A-Z0-9\/\-]+)',
            r'(?:No|NO)\s*:\s*([A-Z0-9\/\-\.]+)',
            r'([0-9]{3,}\/[A-Z0-9\/\-]+)',  # Format: 045/KWT/KRS/III/2026
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                inv = match.group(1).strip()
                inv = re.sub(r'\s+', '', inv)
                if len(inv) > 2:
                    return inv[:50]
        
        return None
    
    def extract_invoice_date(self, text):
        """Extract tanggal kwitansi"""
        keywords = ['tanggal', 'date', 'kwitansi', 'invoice', 'tgl']
        return self._extract_date(text, keywords)
    
    def extract_total_cost(self, text):
        """Extract total biaya dalam rupiah"""
        patterns = [
            r'(?:TOTAL|JUMLAH|AMOUNT|BIAYA|BAYAR)[\s\.:]*Rp\.?\s*([0-9]+(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?)',
            r'Rp[\s\.]*([0-9]+(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?)',
            r'([0-9]+[.,][0-9]+(?:[.,][0-9]{3})*)\s*(?:rupiah|rp)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                cost_str = match.group(1)
                # Clean separators
                parts = re.split(r'[.,]', cost_str)
                if len(parts) > 1 and len(parts[-1]) <= 2:
                    cost_str = ''.join(parts[:-1]) + '.' + parts[-1]
                else:
                    cost_str = ''.join(parts)
                
                try:
                    return int(float(cost_str.replace(',', '.')))
                except:
                    pass
        
        return None
    
    def extract_patient_name(self, text):
        """Extract nama pasien"""
        patterns = [
            r'(?:NAMA\s+)?PASIEN\s*[:\.]?\s*([A-Z][a-zA-Z\s\-\.]+?)(?:\n|$)',
            r'(?:PATIENT|NAMA)[\s\.:]*([A-Z][a-zA-Z\s\-\.]+?)(?:\n|$)',
            r'PASIEN\s+ATAS\s+NAMA\s+([A-Z][a-zA-Z\s\-\.]+?)(?:\n|$)',
            r'Nama\s*[:.]?\s*([A-Z][a-zA-Z\s\-\.]+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                # Remove extra fields
                name = re.sub(r'\s+(NIK|UMUR|TTL|JENIS|KELAMIN|DEPT|DEPARTMENT|NO|NOMOR).*$/i', '', name, flags=re.IGNORECASE)
                name = re.sub(r'\s+', ' ', name)
                if len(name) > 2:
                    return name[:100]
        
        return None
    
    def extract_kwitansi_all(self, ocr_text):
        """Extract semua field untuk KWITANSI"""
        return {
            'hospital_name': self.extract_hospital_name(ocr_text),
            'invoice_number': self.extract_invoice_number(ocr_text),
            'invoice_date': self.extract_invoice_date(ocr_text),
            'total_cost': self.extract_total_cost(ocr_text),
            'patient_name': self.extract_patient_name(ocr_text),
        }
    
    # ============================================================
    # SURAT KETERANGAN SAKIT / MEDICAL LETTER EXTRACTION
    # ============================================================
    
    def extract_doctor_name(self, text):
        """Extract nama dokter"""
        patterns = [
            r'(?:DOKTER|DOCTOR|DR\.?|DRRS\.?|SPOG|SP\.PD|SP\.\w+)\s+([A-Z][a-zA-Z\s\.,\-]+?)(?:\n|,\s*Sp|$)',
            r'(?:DOKTER|DOCTOR)[\s\.:]*([A-Z][a-zA-Z\s\.,\-]+?)(?:\n|$)',
            r'dr\.?\s+([A-Z][a-zA-Z\s\.\-,]+?)(?:\n|,|$)',
            r'PERIKSA\s+OLEH\s*[:\.]?\s*([A-Z][a-zA-Z\s\.,\-]+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                name = re.sub(r'[,\s]*Sp.*$', '', name, flags=re.IGNORECASE)
                name = re.sub(r'\s+', ' ', name)
                if len(name) > 2:
                    return name[:100]
        
        return None
    
    def extract_diagnosis(self, text):
        """Extract diagnosa/diagnosis"""
        patterns = [
            r'(?:DIAGNOSIS|DIAGNOSA|PENYAKIT|KELUHAN)[\s\.:]*([A-Za-z\s\.,\-\(]+?)(?:\n|\d|-|DOKTER|DOCTOR|$)',
            r'(?:DIAGNOSIS|DIAGNOSA)\s*[:\.]?\s*([A-Za-z\s\-\.\,]+?)(?:\n|$)',
            r'(?:KELUHAN|COMPLAINT)\s*[:\.]?\s*([A-Za-z\s\.,\-]+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                diag = match.group(1).strip()
                diag = re.sub(r'\s+', ' ', diag)
                if len(diag) > 2:
                    return diag[:200]
        
        return None
    
    def extract_sick_date_from(self, text):
        """Extract tanggal mulai sakit (dari)"""
        keywords = ['dari', 'mulai', 'from', 'start', 'sejak', 'tgl mulai']
        return self._extract_date(text, keywords)
    
    def extract_sick_date_to(self, text):
        """Extract tanggal selesai sakit (sampai)"""
        keywords = ['sampai', 'selesai', 'to', 'end', 'until', 'sd', 's/d', 'tgl akhir']
        return self._extract_date(text, keywords)
    
    def extract_surat_all(self, ocr_text):
        """Extract semua field untuk SURAT KETERANGAN SAKIT"""
        return {
            'doctor_name': self.extract_doctor_name(ocr_text),
            'diagnosis': self.extract_diagnosis(ocr_text),
            'sick_date_from': self.extract_sick_date_from(ocr_text),
            'sick_date_to': self.extract_sick_date_to(ocr_text),
        }
    
    # ============================================================
    # HELPER METHODS
    # ============================================================
    
    def _extract_date(self, text, keywords=None):
        """Generic date extraction dengan keyword context"""
        if keywords is None:
            keywords = []
        
        # Try each date pattern
        for pattern in self.date_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            
            # If have keywords, prefer matches near keywords
            if keywords and matches:
                for match in matches:
                    context = text[max(0, match.start()-50):match.end()+50].lower()
                    if any(kw.lower() in context for kw in keywords):
                        return self._parse_date(match.group(0))
            
            # Fallback to first match
            if matches:
                return self._parse_date(matches[0].group(0))
        
        return None
    
    def _parse_date(self, date_str):
        """Parse various date formats to YYYY-MM-DD"""
        try:
            # Try DD Bulan YYYY format
            match = re.match(r'(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})', date_str, re.IGNORECASE)
            if match:
                day, month_str, year = match.groups()
                month = self.month_map.get(month_str.lower())
                if month:
                    return f"{year}-{month}-{int(day):02d}"
            
            # Try DD/MM/YYYY or DD-MM-YYYY
            match = re.match(r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})', date_str)
            if match:
                day, month, year = match.groups()
                if len(year) == 2:
                    year = '20' + year if int(year) < 50 else '19' + year
                return f"{year}-{int(month):02d}-{int(day):02d}"
            
            # Try YYYY-MM-DD
            match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
            if match:
                year, month, day = match.groups()
                return f"{year}-{int(month):02d}-{int(day):02d}"
        
        except Exception as e:
            print(f"Date parse error: {e}")
        
        return None
    
    def extract_all(self, ocr_text, doc_type='auto'):
        """Extract all fields with auto-detection"""
        text_lower = ocr_text.lower()
        
        # Auto-detect document type
        if doc_type == 'auto':
            if 'kwitansi' in text_lower or 'invoice' in text_lower or 'receipt' in text_lower or 'total' in text_lower:
                doc_type = 'kwitansi'
            elif 'surat' in text_lower or 'dokter' in text_lower or 'diagnosis' in text_lower or 'sakit' in text_lower:
                doc_type = 'surat'
            else:
                doc_type = 'kwitansi'  # Default
        
        result = {'type': doc_type, 'raw_text': ocr_text}
        
        if doc_type == 'kwitansi':
            result.update(self.extract_kwitansi_all(ocr_text))
        elif doc_type == 'surat':
            result.update(self.extract_surat_all(ocr_text))
        
        return result
