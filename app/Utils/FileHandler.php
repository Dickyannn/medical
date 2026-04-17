<?php

namespace App\Utils;

use Illuminate\Http\UploadedFile;

/**
 * File handling utilities for medical document uploads
 */
class FileHandler
{
    const ALLOWED_FORMATS = ['pdf', 'jpg', 'jpeg', 'png'];
    const ALLOWED_MIMES = ['application/pdf', 'image/jpeg', 'image/png'];
    const MAX_FILE_SIZE = 51200; // 50MB in KB
    const MAX_FILE_SIZE_BYTES = 52428800; // 50MB in bytes

    /**
     * Validate uploaded file
     */
    public static function validate(UploadedFile $file): array
    {
        $errors = [];
        
        // Check file size
        if ($file->getSize() > self::MAX_FILE_SIZE_BYTES) {
            $errors[] = "File terlalu besar. Maksimal 50MB, file ini " . round($file->getSize() / 1024 / 1024, 2) . "MB";
        }

        // Check file extension
        $extension = strtolower($file->getClientOriginalExtension());
        if (!in_array($extension, self::ALLOWED_FORMATS)) {
            $errors[] = "Format file tidak didukung. Format yang diperbolehkan: " . implode(', ', self::ALLOWED_FORMATS);
        }

        // Check MIME type
        $mimeType = $file->getMimeType();
        if (!in_array($mimeType, self::ALLOWED_MIMES)) {
            $errors[] = "Tipe file tidak valid. MIME type: " . $mimeType;
        }

        // Check if file is actually uploaded
        if (!$file->isValid()) {
            $errors[] = "File gagal diupload. Error: " . $file->getErrorMessage();
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors,
        ];
    }

    /**
     * Convert file to Base64 string with MIME type prefix
     */
    public static function toBase64(UploadedFile $file): string
    {
        $fileContent = file_get_contents($file->getRealPath());
        $mimeType = $file->getMimeType();
        return 'data:' . $mimeType . ';base64,' . base64_encode($fileContent);
    }

    /**
     * Convert Base64 string back to file temporarily for processing
     */
    public static function fromBase64(string $base64String): ?string
    {
        // Remove data URI prefix if present
        if (strpos($base64String, 'data:') === 0) {
            $base64String = preg_replace('/^data:.*?;base64,/', '', $base64String);
        }

        $fileContent = base64_decode($base64String, true);
        if ($fileContent === false) {
            return null;
        }

        // Create temporary file
        $tempFile = tmpfile();
        fwrite($tempFile, $fileContent);
        stream_get_meta_data($tempFile)['uri'];
        
        return stream_get_meta_data($tempFile)['uri'];
    }

    /**
     * Calculate file hash (SHA256)
     */
    public static function calculateHash(UploadedFile $file): string
    {
        return hash_file('sha256', $file->getRealPath());
    }

    /**
     * Calculate Base64 hash (for comparison)
     */
    public static function calculateBase64Hash(string $base64String): string
    {
        if (strpos($base64String, 'data:') === 0) {
            $base64String = preg_replace('/^data:.*?;base64,/', '', $base64String);
        }
        return hash('sha256', $base64String);
    }

    /**
     * Get file size in readable format
     */
    public static function formatSize(int $bytes): string
    {
        if ($bytes < 1024) {
            return $bytes . ' B';
        } elseif ($bytes < 1024 * 1024) {
            return round($bytes / 1024, 2) . ' KB';
        } else {
            return round($bytes / 1024 / 1024, 2) . ' MB';
        }
    }

    /**
     * Get MIME type from file extension
     */
    public static function getMimeTypeFromExtension(string $extension): ?string
    {
        $mimeTypes = [
            'pdf' => 'application/pdf',
            'jpg' => 'image/jpeg',
            'jpeg' => 'image/jpeg',
            'png' => 'image/png',
        ];

        return $mimeTypes[strtolower($extension)] ?? null;
    }

    /**
     * Sanitize filename
     */
    public static function sanitizeFilename(string $filename): string
    {
        // Remove invalid characters
        $filename = preg_replace('/[^a-zA-Z0-9._-]/', '_', $filename);
        // Remove multiple dots
        $filename = preg_replace('/\.{2,}/', '.', $filename);
        // Limit length to 255 characters
        return substr($filename, 0, 255);
    }

    /**
     * Generate unique filename
     */
    public static function generateUniqueFilename(string $originalFilename): string
    {
        $pathinfo = pathinfo($originalFilename);
        $extension = strtolower($pathinfo['extension']);
        $name = preg_replace('/[^a-zA-Z0-9._-]/', '_', $pathinfo['filename']);
        
        return $name . '_' . time() . '_' . uniqid() . '.' . $extension;
    }

    /**
     * Check if Base64 string is valid
     */
    public static function isValidBase64(string $string): bool
    {
        if (strpos($string, 'data:') === 0) {
            $string = preg_replace('/^data:.*?;base64,/', '', $string);
        }

        return base64_decode($string, true) !== false;
    }

    /**
     * Get Base64 MIME type
     */
    public static function getBase64MimeType(string $base64String): ?string
    {
        if (preg_match('/^data:([^;]+);base64,/', $base64String, $matches)) {
            return $matches[1];
        }
        return null;
    }

    /**
     * Convert file to Base64 without MIME prefix (for storage optimization)
     */
    public static function toBase64Raw(UploadedFile $file): string
    {
        $fileContent = file_get_contents($file->getRealPath());
        return base64_encode($fileContent);
    }

    /**
     * Reconstruct Base64 with MIME type
     */
    public static function reconstructBase64(string $base64Raw, string $mimeType): string
    {
        return 'data:' . $mimeType . ';base64,' . $base64Raw;
    }
}
