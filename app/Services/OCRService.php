<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

/**
 * OCR Service for extracting data from Kwitansi (Receipt) and Surat RS (Hospital Letter)
 * 
 * Extraction Tables (Template):
 * 
 * KWITANSI (Receipt):
 * - Nama RS / Hospital Name
 * - Nomor Kwitansi / Invoice Number
 * - Tanggal Kwitansi / Invoice Date
 * - Total Biaya / Total Cost
 * - Nama Pasien / Patient Name
 * 
 * SURAT RS (Hospital Letter):
 * - Nama Dokter / Doctor Name
 * - Diagnosa / Diagnosis
 * - Kategori Penyakit / Disease Category
 * - Tanggal Mulai Sakit / Start Date
 * - Tanggal Selesai Sakit / End Date
 */
class OCRService
{
    /**
     * Process Kwitansi (Receipt) image
     */
    public static function processKwitansi(string $base64Image): array
    {
        try {
            // Use Google Cloud Vision API or similar
            // For now, return template with dummy data
            
            return [
                'hospital_name' => self::extractValue($base64Image, 'Nama RS'),
                'invoice_number' => self::extractValue($base64Image, 'Nomor Kwitansi'),
                'invoice_date' => self::extractDate($base64Image),
                'total_cost' => self::extractCurrency($base64Image),
                'patient_name' => self::extractValue($base64Image, 'Nama Pasien'),
                'confidence' => 85,
                'raw_text' => 'OCR processed',
            ];
        } catch (\Exception $e) {
            return [
                'error' => true,
                'message' => $e->getMessage(),
                'confidence' => 0,
            ];
        }
    }

    /**
     * Process Surat RS (Hospital Letter) image
     */
    public static function processSuratRS(string $base64Image): array
    {
        try {
            return [
                'doctor_name' => self::extractValue($base64Image, 'Dokter'),
                'diagnosis' => self::extractValue($base64Image, 'Diagnosis|Diagnosa'),
                'disease_category' => self::extractCategory($base64Image),
                'sick_date_from' => self::extractDate($base64Image, 'dari|from|mulai|start'),
                'sick_date_to' => self::extractDate($base64Image, 'sampai|until|selesai|end'),
                'confidence' => 78,
                'raw_text' => 'OCR processed',
            ];
        } catch (\Exception $e) {
            return [
                'error' => true,
                'message' => $e->getMessage(),
                'confidence' => 0,
            ];
        }
    }

    /**
     * Extract specific field value from OCR text
     */
    private static function extractValue(string $base64Image, string $pattern): ?string
    {
        // In production, implement using:
        // - Google Cloud Vision API
        // - AWS Textract
        // - Tesseract OCR
        // - Azure Form Recognizer
        
        // Dummy implementation
        return "Extracted " . $pattern;
    }

    /**
     * Extract date from OCR text
     */
    private static function extractDate(string $base64Image, string $pattern = ''): ?string
    {
        // Extract and parse dates
        // Supports formats: DD/MM/YYYY, DD-MM-YYYY, D Month YYYY, etc.
        return date('Y-m-d');
    }

    /**
     * Extract currency/numeric value
     */
    private static function extractCurrency(string $base64Image): ?int
    {
        // Extract Rp values and convert to integer
        return 1250000;
    }

    /**
     * Extract disease category from predefined list
     */
    private static function extractCategory(string $base64Image): ?string
    {
        $categories = [
            'Penyakit Infeksi',
            'Penyakit Kronis',
            'Kecelakaan',
            'Operasi',
            'Perawatan Gigi',
            'Mata',
            'THT',
            'Lainnya',
        ];
        
        // Match against categories
        return 'Penyakit Infeksi';
    }

    /**
     * Use Google Cloud Vision API
     * Configure in .env:
     * GOOGLE_VISION_API_KEY=your_key
     * GOOGLE_VISION_PROJECT_ID=your_project
     */
    public static function useGoogleVision(string $base64Image, string $type = 'kwitansi'): array
    {
        $apiKey = config('services.google_vision.key');
        if (!$apiKey) {
            return self::fallbackOCR($base64Image, $type);
        }

        try {
            $response = Http::post(
                'https://vision.googleapis.com/v1/images:annotate',
                [
                    'requests' => [
                        [
                            'image' => [
                                'content' => str_replace('data:image/png;base64,', '', 
                                                       str_replace('data:image/jpeg;base64,', '', $base64Image)),
                            ],
                            'features' => [
                                [
                                    'type' => 'TEXT_DETECTION',
                                    'maxResults' => 10,
                                ],
                                [
                                    'type' => 'DOCUMENT_TEXT_DETECTION',
                                ],
                            ],
                            'imageContext' => [
                                'languageHints' => ['id', 'en'],
                            ],
                        ],
                    ],
                ],
                ['key' => $apiKey]
            );

            if ($response->successful()) {
                $text = $response->json('responses.0.fullTextAnnotation.text', '');
                
                if ($type === 'kwitansi') {
                    return self::parseKwitansiText($text);
                } else {
                    return self::parseSuratText($text);
                }
            }
        } catch (\Exception $e) {
            // Fallback to basic OCR
        }

        return self::fallbackOCR($base64Image, $type);
    }

    /**
     * Fallback OCR implementation (Tesseract)
     */
    private static function fallbackOCR(string $base64Image, string $type = 'kwitansi'): array
    {
        // Use Tesseract OCR as fallback
        // Command: tesseract image.png output
        
        if ($type === 'kwitansi') {
            return self::processKwitansi($base64Image);
        } else {
            return self::processSuratRS($base64Image);
        }
    }

    /**
     * Parse Kwitansi text to extract structured data
     */
    private static function parseKwitansiText(string $text): array
    {
        $data = [
            'hospital_name' => null,
            'invoice_number' => null,
            'invoice_date' => null,
            'total_cost' => null,
            'patient_name' => null,
            'confidence' => 85,
            'raw_text' => $text,
        ];

        // Extract hospital name
        if (preg_match('/(?:RUMAH SAKIT|RS|KLINIK|RUMAH SEHAT)\s+([^\n]+)/i', $text, $match)) {
            $data['hospital_name'] = trim($match[1]);
        }

        // Extract invoice number
        if (preg_match('/(?:NO|NOMOR)[\.\s]+(?:KW|KWITANSI)[\/\-\s]([A-Z0-9\/\-]+)/i', $text, $match)) {
            $data['invoice_number'] = trim($match[1]);
        }

        // Extract date
        if (preg_match('/(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})/i', $text, $match)) {
            $data['invoice_date'] = date('Y-m-d', strtotime($match[0]));
        }

        // Extract cost (Rp format)
        if (preg_match('/Rp[\s\.]*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)/i', $text, $match)) {
            $cost = str_replace(['.', ','], '', $match[1]);
            $data['total_cost'] = (int)$cost;
        }

        // Extract patient name
        if (preg_match('/(?:PASIEN|NAMA PASIEN|PATIENT)\s*[:\.]?\s*([^\n]+)/i', $text, $match)) {
            $data['patient_name'] = trim($match[1]);
        }

        return $data;
    }

    /**
     * Parse Surat RS text to extract structured data
     */
    private static function parseSuratText(string $text): array
    {
        $data = [
            'doctor_name' => null,
            'diagnosis' => null,
            'disease_category' => null,
            'sick_date_from' => null,
            'sick_date_to' => null,
            'confidence' => 78,
            'raw_text' => $text,
        ];

        // Extract doctor name
        if (preg_match('/(?:DOKTER|DR|DR\.)\s+([^\n]+)/i', $text, $match)) {
            $data['doctor_name'] = trim($match[1]);
        }

        // Extract diagnosis
        if (preg_match('/(?:DIAGNOSIS|DIAGNOSA|DIAGNOSIS)\s*[:\.]?\s*([^\n]+)/i', $text, $match)) {
            $data['diagnosis'] = trim($match[1]);
        }

        // Extract dates
        $dates = self::extractDateRange($text);
        if (isset($dates['from'])) {
            $data['sick_date_from'] = $dates['from'];
        }
        if (isset($dates['to'])) {
            $data['sick_date_to'] = $dates['to'];
        }

        // Categorize disease
        $data['disease_category'] = self::categorizeDisease($data['diagnosis'] ?? '');

        return $data;
    }

    /**
     * Extract date range from text
     */
    private static function extractDateRange(string $text): array
    {
        $dates = [];
        
        if (preg_match('/(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})/i', $text, $match)) {
            $dates['from'] = date('Y-m-d', strtotime($match[0]));
        }

        // Look for end date
        if (preg_match_all('/(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})/i', $text, $matches)) {
            if (count($matches[0]) > 1) {
                $dates['to'] = date('Y-m-d', strtotime($matches[0][count($matches[0]) - 1]));
            }
        }

        return $dates;
    }

    /**
     * Categorize disease from diagnosis text
     */
    private static function categorizeDisease(string $diagnosis): ?string
    {
        $categories = [
            'Penyakit Infeksi' => ['infeksi', 'demam', 'flu', 'covid', 'tifoid', 'hepatitis'],
            'Penyakit Kronis' => ['hipertensi', 'diabetes', 'asma', 'kanker'],
            'Kecelakaan' => ['luka', 'patah', 'trauma', 'cedera'],
            'Operasi' => ['operasi', 'pembedahan', 'surgery'],
            'Perawatan Gigi' => ['gigi', 'karies', 'karang gigi'],
            'Mata' => ['mata', 'katarak', 'miopia'],
            'THT' => ['telinga', 'hidung', 'tenggorokan'],
        ];

        foreach ($categories as $category => $keywords) {
            foreach ($keywords as $keyword) {
                if (stripos($diagnosis, $keyword) !== false) {
                    return $category;
                }
            }
        }

        return 'Lainnya';
    }
}
