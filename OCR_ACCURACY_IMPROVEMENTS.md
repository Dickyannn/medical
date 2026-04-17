# OCR Accuracy Improvements

## Summary
Enhanced the OCR parsing methods in `SubmissionController.php` to better extract data from Indonesian medical documents without hardcoding values.

## Changes Made

### 1. Enhanced `parseSuratText()` Method

#### Doctor Name Extraction
- **Improved**: Better handling of "dr." prefix with Indonesian names
- **Added**: More keyword patterns: "DOKTER:", "DIPERIKSA OLEH", "YANG MEMERIKSA"
- **Fixed**: Now properly extracts "dr. Andi Pratama" format
- **Cleaned**: Removes specializations (Sp.PD, SIP, M.Kes) automatically

**Example**: 
- Input: "DOKTER: dr. Andi Pratama, Sp.PD"
- Output: "dr. Andi Pratama"

#### Diagnosis Extraction
- **Enhanced**: Now handles compound diagnoses with parentheses and "dan"
- **Improved**: Better text boundary detection to avoid capturing unrelated text
- **Added**: Fallback pattern for "menderita" keyword
- **Increased**: Max length from 100 to 150 characters for complex diagnoses

**Example**:
- Input: "DIAGNOSIS: Influenza (Flu) dan Demam"
- Output: "Influenza (Flu) dan Demam"

#### Date Range Extraction
- **Added**: Support for "s.d." separator (sampai dengan)
- **Enhanced**: Primary pattern to catch dates before keyword matching
- **Improved**: Better handling of Indonesian date formats
- **Added**: Multiple separator support: "s.d.", "s/d", "sd", "sampai dengan", "hingga"

**Example**:
- Input: "4 Maret 2026 s.d. 6 Maret 2026"
- Output: From: "2026-03-04", To: "2026-03-06"

### 2. Enhanced Disease Categorization

#### Added Keywords
- **Influenza**: Added "influenza", "common cold", "selesma"
- **Fever**: Added "panas", "fever"
- Better matching for compound diagnoses like "Influenza (Flu) dan Demam"

**Example**:
- Input: "Influenza (Flu) dan Demam"
- Category: "Penyakit Infeksi"

### 3. Existing Kwitansi Enhancements (Already Implemented)

The `parseKwitansiText()` method was previously enhanced with:
- Multiple hospital name patterns (including "Admin Klinik")
- Better invoice number extraction
- Enhanced date parsing with fallbacks
- Improved total cost extraction (finds largest amount if keyword fails)
- Better patient name extraction with "Telah diterima dari" pattern

## How It Works

### Keyword-Based Extraction Strategy
1. **Primary Pattern**: Look for specific keywords followed by data
2. **Fallback Pattern**: Use alternative keywords or patterns
3. **Context Cleaning**: Remove unwanted text (specializations, line breaks)
4. **Validation**: Check length and format before accepting

### No Hardcoding
- All extraction is pattern-based using regex
- Multiple fallback patterns for robustness
- Handles variations in document formats
- Returns `null` if data cannot be extracted (no fake data)

## Testing with Your Images

### Kwitansi Image
Expected to extract:
- Hospital: "Klinik Sehat Sentosa"
- Invoice No: "012/KWT/KSS/III/2026"
- Patient: "Budi Santoso"
- Total: "150000" (Rp 150.000)
- Date: "2026-03-04" (4 Maret 2026)

### Surat Keterangan Sakit Image
Expected to extract:
- Doctor: "dr. Andi Pratama"
- Diagnosis: "Influenza (Flu) dan Demam"
- Date From: "2026-03-04" (4 Maret 2026)
- Date To: "2026-03-06" (6 Maret 2026)
- Category: "Penyakit Infeksi"

## Next Steps

1. **Test with actual images**: Upload your test images to see the improved extraction
2. **Check logs**: Review Laravel logs to see what patterns matched
3. **Fine-tune**: If some fields are still empty, check the logs to see what text was extracted and adjust patterns accordingly

## Debugging Tips

If fields are still empty:
1. Check `storage/logs/laravel.log` for OCR text preview
2. Look for "Parsing surat text" and "Parsing kwitansi text" entries
3. See which patterns matched or failed
4. The raw OCR text is logged with preview (first 500 chars)

## Technical Details

**Files Modified**:
- `app/Http/Controllers/SubmissionController.php`
  - `parseSuratText()` method (lines ~715-850)
  - `categorizeDisease()` method (lines ~950-1000)

**Regex Patterns Used**:
- Case-insensitive matching (`/i` flag)
- Flexible whitespace handling (`\s+`, `\s*`)
- Multiple separator support (`(?:-|s\.d\.|s\/d|sampai|hingga)`)
- Boundary detection to avoid over-capturing

**No Breaking Changes**:
- All changes are backward compatible
- Existing functionality preserved
- Only enhanced pattern matching
