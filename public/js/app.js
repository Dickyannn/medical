/**
 * MedClaim — Medical Management System
 * Core Application Data & Utilities
 */

// ════════════════════════════════════════════════
// SAMPLE DATA
// ════════════════════════════════════════════════

const users = {
  ga: {
    name: 'Ahmad Syafii',
    initials: 'AS',
    roleName: 'GA (Pengajuan)',
    email: 'ga@perusahaan.id',
    department: 'Engineering'
  },
  reviewer: {
    name: 'Siti Rahayu',
    initials: 'SR',
    roleName: 'Reviewer',
    email: 'reviewer@perusahaan.id',
    department: 'Medical Admin'
  },
  fa: {
    name: 'Budi Santoso',
    initials: 'BS',
    roleName: 'F&A (Keuangan)',
    email: 'fa@perusahaan.id',
    department: 'Finance'
  }
};

const submissions = [
  {
    id: 'S001',
    employee: 'Budi Santoso',
    nik: '10234',
    rs: 'RS Siloam Kebon Jeruk',
    diagnosis: 'Demam Tifoid',
    date: '8–12 Apr 2025',
    cost: 'Rp 1.250.000',
    status: 'completed',
    hasStamp: true,
    createdBy: 'ga',
    reviewedBy: 'reviewer',
    ocrScore: 92,
    duplicateFlag: false
  },
  {
    id: 'S002',
    employee: 'Siti Rahayu',
    nik: '10235',
    rs: 'RSUD Tarakan',
    diagnosis: 'Infeksi Saluran Napas',
    date: '5–7 Apr 2025',
    cost: 'Rp 480.000',
    status: 'stamped',
    hasStamp: false,
    createdBy: 'ga',
    reviewedBy: 'reviewer',
    ocrScore: 88,
    duplicateFlag: false
  },
  {
    id: 'S003',
    employee: 'Hendra Wijaya',
    nik: '10236',
    rs: 'RS Pondok Indah',
    diagnosis: 'Gastritis Akut',
    date: '2–4 Apr 2025',
    cost: 'Rp 730.000',
    status: 'approved',
    hasStamp: false,
    createdBy: 'ga',
    reviewedBy: 'reviewer',
    ocrScore: 85,
    duplicateFlag: false
  },
  {
    id: 'S004',
    employee: 'Hendra Wijaya',
    nik: '10236',
    rs: 'RS Siloam Kebon Jeruk',
    diagnosis: 'Migrain Kronis',
    date: '15–16 Apr 2025',
    cost: 'Rp 620.000',
    status: 'rejected',
    hasStamp: false,
    createdBy: 'ga',
    reviewedBy: 'reviewer',
    ocrScore: 62,
    duplicateFlag: false,
    rejectionReason: 'Kwitansi tidak terbaca, harap scan ulang dengan resolusi lebih tinggi.'
  },
  {
    id: 'S005',
    employee: 'Putra Mandiri',
    nik: '10237',
    rs: 'RS Siloam Semanggi',
    diagnosis: 'Hipertensi',
    date: '10–11 Apr 2025',
    cost: 'Rp 215.000',
    status: 'duplicate_flagged',
    hasStamp: false,
    createdBy: 'ga',
    reviewedBy: 'reviewer',
    ocrScore: 91,
    duplicateFlag: true,
    duplicateOf: 'S001'
  },
  {
    id: 'S006',
    employee: 'Rina Wijayanti',
    nik: '10238',
    rs: 'RSUD Tarakan',
    diagnosis: 'Asma Akut',
    date: '13–14 Apr 2025',
    cost: 'Rp 395.000',
    status: 'pending_review',
    hasStamp: false,
    createdBy: 'ga',
    reviewedBy: null,
    ocrScore: 86,
    duplicateFlag: false
  }
];

// ════════════════════════════════════════════════
// SESSION STATE
// ════════════════════════════════════════════════

let currentRole = null;
let currentTab = null;
let uploadStep = 1;

// Initialize window globals
window.selectedFiles = {};
window.currentSubmission = null;

// ════════════════════════════════════════════════
// UTILITIES
// ════════════════════════════════════════════════

function setRole(role) {
  currentRole = role;
  localStorage.setItem('medclaim_role', role);
}

function getRole() {
  return localStorage.getItem('medclaim_role') || currentRole;
}

function initializeApp(role) {
  setRole(role);
  const u = users[role];
  document.getElementById('user-avatar').textContent = u.initials;
  document.getElementById('user-name').textContent = u.name;
  const rb = document.getElementById('role-badge');
  rb.textContent = u.roleName;
  rb.className = 'topbar-role role-' + (role === 'reviewer' ? 'reviewer' : role);

  buildNav();
  switchTab(getDefaultTab());
}

function getDefaultTab() {
  if (currentRole === 'ga') return 'ga-upload';
  if (currentRole === 'reviewer') return 'rv-queue';
  if (currentRole === 'fa') return 'fa-report';
}

function buildNav() {
  const navs = {
    ga: [
      { id: 'ga-upload', label: 'Upload Dokumen', icon: '📤' },
      { id: 'ga-history', label: 'Riwayat', icon: '📋' },
      { id: 'ga-stamp', label: 'Stempel & Kirim', icon: '🗂️', badge: submissions.filter(s => s.status === 'approved' && !s.hasStamp).length },
    ],
    reviewer: [
      { id: 'rv-queue', label: 'Antrian Review', icon: '📥', badge: submissions.filter(s => s.status === 'pending_review' || s.status === 'duplicate_flagged').length },
      { id: 'rv-history', label: 'Riwayat Review', icon: '📋' },
    ],
    fa: [
      { id: 'fa-report', label: 'Laporan Klaim', icon: '📊' },
      { id: 'fa-summary', label: 'Ringkasan', icon: '📈' },
    ],
  };
  const nav = document.getElementById('topbar-nav');
  nav.innerHTML = '';
  (navs[currentRole] || []).forEach(n => {
    const b = document.createElement('button');
    b.className = 'nav-btn';
    b.id = 'nav-' + n.id;
    b.onclick = () => switchTab(n.id);
    b.innerHTML = n.icon + ' ' + n.label + (n.badge ? ` <span class="nav-badge">${n.badge}</span>` : '');
    nav.appendChild(b);
  });
}

function switchTab(tabId) {
  try {
    console.log('switchTab called with tabId:', tabId);
    currentTab = tabId;
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    const nb = document.getElementById('nav-' + tabId);
    if (nb) nb.classList.add('active');

    const content = document.getElementById('app-content');
    if (!content) {
      throw new Error('app-content element not found');
    }
    content.innerHTML = '';
    content.className = 'animate-in';

    const renders = {
      'ga-upload': renderGAUpload,
      'ga-history': renderGAHistory,
      'ga-stamp': renderGAStamp,
      'rv-queue': renderRVQueue,
      'rv-history': renderRVHistory,
      'fa-report': renderFAReport,
      'fa-summary': renderFASummary,
    };
    
    if (renders[tabId]) {
      console.log('Calling render function for:', tabId);
      renders[tabId](content);
      console.log('Render function completed');
    } else {
      throw new Error('No render function found for tabId: ' + tabId);
    }
  } catch (error) {
    console.error('Error in switchTab:', error);
    const content = document.getElementById('app-content');
    if (content) {
      content.innerHTML = `<div style="color:red;padding:20px;"><h3>Error: ${error.message}</h3><pre>${error.stack}</pre></div>`;
    }
  }
}

function openModal(id) {
  document.getElementById(id).classList.add('open');
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

function goStep(n) {
  uploadStep = n;
  switchTab('ga-upload');
}

function selectFile(type) {
  // Trigger file input
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.pdf,.jpg,.jpeg,.png';
  input.onchange = function(e) {
    handleFileSelect(type, e.target.files[0]);
  };
  input.click();
}

async function handleFileSelect(type, file) {
  if (!file) return;

  const validation = validateFile(file);
  if (!validation.valid) {
    alert('❌ File Error:\n' + validation.errors.join('\n'));
    return;
  }

  // Store file for later upload
  if (!window.selectedFiles) window.selectedFiles = {};
  window.selectedFiles[type] = file;

  // Hide upload area and show file info
  const uploadArea = document.getElementById('ua-' + type);
  const fileDiv = document.getElementById('file-' + type);
  
  if (uploadArea) uploadArea.style.display = 'none';
  if (fileDiv) {
    fileDiv.style.display = 'block';
    fileDiv.innerHTML = `
      <div class="flex items-center gap-2">
        <span style="font-size:1.2rem">📎</span>
        <div style="flex:1">
          <div class="text-sm font-medium">${file.name}</div>
          <div class="text-xs text-faint">${formatFileSize(file.size)} • Siap diproses</div>
        </div>
        <span style="color:${type === 'kwitansi' ? 'var(--accent)' : 'var(--info)'};font-size:1rem">✓</span>
      </div>
    `;
  }
}

function validateFile(file) {
  const maxSize = 50 * 1024 * 1024; // 50MB
  const allowedFormats = ['pdf', 'jpg', 'jpeg', 'png'];
  const allowedMimes = ['application/pdf', 'image/jpeg', 'image/png'];
  
  const errors = [];
  
  if (file.size > maxSize) {
    errors.push(`File terlalu besar (${formatFileSize(file.size)}, max 50MB)`);
  }
  
  const ext = file.name.split('.').pop().toLowerCase();
  if (!allowedFormats.includes(ext)) {
    errors.push(`Format tidak didukung. Gunakan: ${allowedFormats.join(', ')}`);
  }
  
  if (!allowedMimes.includes(file.type)) {
    errors.push(`Tipe file tidak valid (${file.type})`);
  }
  
  return {
    valid: errors.length === 0,
    errors: errors
  };
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / 1024 / 1024).toFixed(2) + ' MB';
}

async function submitDoc() {
  if (!window.selectedFiles || !window.selectedFiles.kwitansi || !window.selectedFiles.surat) {
    alert('❌ Silakan pilih kedua file terlebih dahulu!');
    return;
  }
  
  // Get form values with specific IDs
  const employeeName = document.getElementById('employee-name')?.value?.trim();
  const nikEmployee = document.getElementById('employee-nik')?.value?.trim();
  const department = document.getElementById('employee-department')?.value;
  const relationType = document.getElementById('employee-relation')?.value;
  
  console.log('Form values:', { employeeName, nikEmployee, department, relationType });
  
  if (!employeeName || !nikEmployee || !department || !relationType) {
    alert('❌ Lengkapi semua data karyawan terlebih dahulu!');
    return;
  }
  
  // Show loading state
  const submitBtn = event?.target;
  let originalText = '';
  if (submitBtn) {
    originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⏳ Memproses OCR...';
  }
  
  const formData = new FormData();
  formData.append('employee_name', employeeName);
  formData.append('nik_employee', nikEmployee);
  formData.append('department', department);
  formData.append('relation_type', relationType === 'Karyawan sendiri' ? 'self' : relationType === 'Suami/Istri' ? 'spouse' : 'child');
  formData.append('kwitansi_file', window.selectedFiles.kwitansi);
  formData.append('surat_file', window.selectedFiles.surat);
  
  try {
    console.log('Sending request to /api/ocr-process...');
    const response = await fetch('/api/ocr-process', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    console.log('Response status:', response.status);
    
    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const text = await response.text();
      console.error('Non-JSON response:', text.substring(0, 500));
      throw new Error('Server mengembalikan response yang tidak valid. Cek console untuk detail.');
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    
    if (response.ok && data.success) {
      // Store OCR results in memory (not in DB yet)
      window.currentSubmission = data.data;
      window.currentSubmission.employee_name = employeeName;
      window.currentSubmission.nik_employee = nikEmployee;
      window.currentSubmission.department = department;
      window.currentSubmission.relation_type = relationType === 'Karyawan sendiri' ? 'self' : relationType === 'Suami/Istri' ? 'spouse' : 'child';
      
      // Move to step 2 for review
      uploadStep = 2;
      switchTab('ga-upload');
    } else {
      throw new Error(data.message || 'OCR processing gagal');
    }
  } catch (error) {
    console.error('Submit error:', error);
    alert('❌ Error: ' + error.message);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  }
}

function doReject() {
  closeModal('modal-reject');
  alert('✗ Pengajuan berhasil ditolak. GA akan mendapat notifikasi.');
  switchTab('rv-queue');
}

function doApprove() {
  closeModal('modal-approve');
  alert('✓ Pengajuan berhasil disetujui! GA akan mendapat notifikasi untuk memberi stempel.');
  switchTab('rv-queue');
}

function doLogout() {
  if (confirm('Apakah Anda yakin ingin keluar?')) {
    localStorage.removeItem('medclaim_role');
    window.location.href = '/login.html';
  }
}

// ════════════════════════════════════════════════
// API Functions for Real Data Loading
// ════════════════════════════════════════════════

async function loadMySubmissions() {
  try {
    const response = await fetch('/api/my-submissions');
    if (response.ok) {
      const data = await response.json();
      return data.data || [];
    }
  } catch (error) {
    console.error('Error loading submissions:', error);
  }
  return [];
}

async function loadPendingReviews() {
  try {
    const response = await fetch('/api/pending-reviews');
    if (response.ok) {
      const data = await response.json();
      return data.data || [];
    }
  } catch (error) {
    console.error('Error loading pending reviews:', error);
  }
  return [];
}

async function loadSubmission(submissionId) {
  try {
    const response = await fetch(`/api/submissions/${submissionId}`);
    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        window.currentSubmission = result.data;
        uploadStep = 2; // Move to OCR review step
        switchTab('ga-upload');
        return result.data;
      }
    }
    throw new Error('Failed to load submission');
  } catch (error) {
    console.error('Error loading submission:', error);
    alert('❌ Gagal memuat data submission: ' + error.message);
  }
  return null;
}

async function confirmAndSubmit() {
  // This is where we actually save to DB and check for duplicates
  if (!window.currentSubmission) {
    alert('❌ Data submission tidak ditemukan');
    return;
  }
  
  // Show loading
  const submitBtn = event?.target;
  let originalText = '';
  if (submitBtn) {
    originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⏳ Menyimpan & Cek Duplikasi...';
  }
  
  // Collect edited values from OCR fields using IDs
  const submissionData = {
    // Employee data
    employee_name: window.currentSubmission.employee_name,
    nik_employee: window.currentSubmission.nik_employee,
    department: window.currentSubmission.department,
    relation_type: window.currentSubmission.relation_type,
    
    // Images (Base64)
    kwitansi_image_base64: window.currentSubmission.kwitansi_image,
    surat_image_base64: window.currentSubmission.surat_image,
    
    // OCR data (edited by user)
    patient_name: document.getElementById('ocr-patient')?.value || window.currentSubmission.patient_name,
    hospital_name: document.getElementById('ocr-hospital')?.value || window.currentSubmission.hospital_name,
    invoice_number: document.getElementById('ocr-invoice')?.value || window.currentSubmission.invoice_number,
    total_cost: parseInt(document.getElementById('ocr-cost')?.value?.replace(/[^\d]/g, '') || '0'),
    invoice_date: document.getElementById('ocr-date')?.value || window.currentSubmission.invoice_date,
    doctor_name: document.getElementById('ocr-doctor')?.value || window.currentSubmission.doctor_name,
    diagnosis: document.getElementById('ocr-diagnosis')?.value || window.currentSubmission.diagnosis,
    sick_date_from: document.getElementById('ocr-date-from')?.value || window.currentSubmission.sick_date_from,
    sick_date_to: document.getElementById('ocr-date-to')?.value || window.currentSubmission.sick_date_to,
    disease_category: document.getElementById('ocr-category')?.value || window.currentSubmission.disease_category,
    
    // OCR metadata
    ocr_confidence_score: window.currentSubmission.ocr_confidence || 85,
    ocr_kwitansi_data: window.currentSubmission.ocr_kwitansi_data,
    ocr_surat_data: window.currentSubmission.ocr_surat_data,
  };
  
  console.log('Saving submission with duplicate check:', submissionData);
  
  try {
    const response = await fetch('/api/submissions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(submissionData)
    });
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      // Check if duplicate was detected
      if (result.data.is_duplicate) {
        const dupPercent = result.data.duplicate_percentage || 0;
        alert(`⚠️ Duplikasi terdeteksi (${dupPercent}% kesamaan)!\n\nPengajuan serupa: ${result.data.similar_submission_id}\nDokumen tetap disimpan dan akan direview secara manual.`);
      } else {
        alert('✓ Dokumen berhasil disimpan dan dikirim ke Reviewer!');
      }
      
      // Reset and go to history
      uploadStep = 1;
      window.selectedFiles = {};
      window.currentSubmission = null;
      switchTab('ga-history');
    } else {
      throw new Error(result.message || 'Gagal menyimpan submission');
    }
  } catch (error) {
    console.error('Confirm submit error:', error);
    alert('❌ Error: ' + error.message);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  }
}

// ════════════════════════════════════════════════
// Utility Functions for Base64 Images
// ════════════════════════════════════════════════

function displayBase64Image(base64String, containerId) {
  const container = document.getElementById(containerId);
  if (container && base64String) {
    container.innerHTML = `<img src="${base64String}" style="width:100%;height:auto;"/>`;
  }
}

function getImagePreviewHTML(base64String, maxHeight = '300px') {
  if (!base64String) return '';
  return `<img src="${base64String}" style="max-height:${maxHeight};width:auto;display:block;margin:0 auto;"/>`;
}
