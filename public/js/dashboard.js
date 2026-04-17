/**
 * MedClaim — Dashboard Render Functions by Role
 * GA • Reviewer • Finance & Admin
 */

// ════════════════════════════════════════════════
// GA — UPLOAD
// ════════════════════════════════════════════════

function renderGAUpload(el) {
  try {
    console.log('renderGAUpload called, uploadStep:', uploadStep);
    
    let html = '<div class="page-header">';
    html += '<h2>Upload Dokumen Klaim Medis</h2>';
    html += '<p>Upload kwitansi dan surat keterangan rumah sakit untuk diproses OCR secara otomatis</p>';
    html += '</div>';
    
    html += '<div class="steps mb-4">';
    html += '<div class="step-item ' + (uploadStep>=1?'active':'') + '">';
    html += '<div class="step-circle">' + (uploadStep>1?'✓':'1') + '</div>Upload Dokumen';
    html += '</div>';
    html += '<div class="step-line ' + (uploadStep>1?'done':'') + '"></div>';
    html += '<div class="step-item ' + (uploadStep>=2?'active':'') + '">';
    html += '<div class="step-circle">' + (uploadStep>2?'✓':'2') + '</div>Proses OCR';
    html += '</div>';
    html += '<div class="step-line ' + (uploadStep>2?'done':'') + '"></div>';
    html += '<div class="step-item ' + (uploadStep>=3?'active':'') + '">';
    html += '<div class="step-circle">3</div>Konfirmasi & Kirim';
    html += '</div>';
    html += '</div>';
    
    if (uploadStep === 1) {
      html += renderUploadStep1();
    } else if (uploadStep === 2) {
      html += renderUploadStep2();
    } else if (uploadStep === 3) {
      html += renderUploadStep3();
    }
    
    el.innerHTML = html;
    console.log('✓ renderGAUpload completed');
  } catch (error) {
    console.error('✗ Error in renderGAUpload:', error);
    el.innerHTML = '<div style="color:red;padding:20px;"><strong>Error:</strong> ' + error.message + '</div>';
  }
}

function renderUploadStep1() {
  return `
  <div class="grid-2 mb-3">
    <div>
      <div class="card-header" style="background:var(--amber-light);border-radius:var(--radius-lg) var(--radius-lg) 0 0;border:1px solid rgba(122,79,0,0.15);border-bottom:1px solid var(--border)">
        <h3 style="color:var(--amber)">🧾 Kwitansi Biaya</h3>
        <span class="badge badge-pending" style="background:var(--amber);color:#fff">Wajib</span>
      </div>
      <div class="card" style="border-radius:0 0 var(--radius-lg) var(--radius-lg);border-top:none;">
        <div class="card-body">
          <div class="upload-area" id="ua-kwitansi" onclick="selectFile('kwitansi')">
            <div class="upload-icon">📄</div>
            <div class="upload-title">Klik atau seret file ke sini</div>
            <div class="upload-sub">PDF, JPG, JPEG, PNG • Max 50 MB</div>
          </div>
          <div id="file-kwitansi" style="display:none;margin-top:10px;padding:10px 14px;background:var(--accent-light);border-radius:var(--radius);border:1px solid rgba(242, 103, 34, 0.15);">
            <!-- File info will be inserted here -->
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="card-header" style="background:var(--info-light);border-radius:var(--radius-lg) var(--radius-lg) 0 0;border:1px solid rgba(10, 48, 80, 0.15);border-bottom:1px solid var(--border)">
        <h3 style="color:var(--info)">📋 Surat Keterangan RS</h3>
        <span class="badge badge-pending" style="background:var(--info);color:#fff">Wajib</span>
      </div>
      <div class="card" style="border-radius:0 0 var(--radius-lg) var(--radius-lg);border-top:none;">
        <div class="card-body">
          <div class="upload-area" id="ua-surat" onclick="selectFile('surat')">
            <div class="upload-icon">📄</div>
            <div class="upload-title">Klik atau seret file ke sini</div>
            <div class="upload-sub">PDF, JPG, JPEG, PNG • Max 50 MB</div>
          </div>
          <div id="file-surat" style="display:none;margin-top:10px;padding:10px 14px;background:var(--info-light);border-radius:var(--radius);border:1px solid rgba(10, 48, 80, 0.15);">
            <!-- File info will be inserted here -->
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card mb-3">
    <div class="card-body">
      <form id="employee-form">
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Nama Karyawan</label>
            <input class="form-input" id="employee-name" name="employee_name" value="" placeholder="Nama lengkap" required>
          </div>
          <div class="form-group">
            <label class="form-label">NIK Karyawan</label>
            <input class="form-input" id="employee-nik" name="nik_employee" value="" placeholder="Nomor induk karyawan" required>
          </div>
          <div class="form-group">
            <label class="form-label">Departemen</label>
            <select class="form-input" id="employee-department" name="department" required>
              <option value="">-- Pilih Departemen --</option>
              <option value="Engineering">Engineering</option>
              <option value="Marketing">Marketing</option>
              <option value="Finance">Finance</option>
              <option value="HR">HR</option>
              <option value="Operations">Operations</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Hubungan</label>
            <select class="form-input" id="employee-relation" name="relation_type" required>
              <option value="">-- Pilih Hubungan --</option>
              <option value="Karyawan sendiri">Karyawan sendiri</option>
              <option value="Suami/Istri">Suami/Istri</option>
              <option value="Anak">Anak</option>
            </select>
          </div>
        </div>
      </form>
    </div>
  </div>

  <div class="flex gap-2" style="justify-content:flex-end">
    <button class="btn btn-primary" onclick="submitDoc()">Upload & Proses OCR →</button>
  </div>
  `;
}

function renderUploadStep2() {
  if (!window.currentSubmission) {
    return '<div class="notif notif-danger mb-3"><span class="notif-icon">✗</span><div>Data submission tidak ditemukan. Silakan upload ulang.</div></div>';
  }
  
  const kwitansiImage = window.currentSubmission.kwitansi_image || '';
  const suratImage = window.currentSubmission.surat_image || '';
  const kConfidence = window.currentSubmission.ocr_confidence || 85;
  const sConfidence = Math.max(0, kConfidence - 10);
  
  console.log('Step 2 - Current Submission:', window.currentSubmission);
  
  return `
  <div class="notif notif-info mb-3">
    <span class="notif-icon">ℹ</span>
    <div><strong>OCR Selesai!</strong> Periksa dan edit data jika diperlukan sebelum mengirim ke Reviewer.</div>
  </div>
  
  <div class="grid-2 mb-3">
    <div class="card">
      <div class="card-header">
        <h3>Hasil OCR — Kwitansi</h3>
        <span class="conf-bar"><span class="conf-track"><span class="conf-fill conf-hi" style="width:${kConfidence}%"></span></span><span class="conf-pct">${kConfidence}%</span></span>
      </div>
      <div class="card-body">
        ${kwitansiImage ? `
          <div style="margin-bottom:12px;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;max-height:400px;display:flex;align-items:center;justify-content:center;background:#f5f5f5;">
            <img src="${kwitansiImage}" style="max-width:100%;max-height:400px;width:auto;height:auto;object-fit:contain;display:block;"/>
          </div>
        ` : '<div style="padding:2rem;text-align:center;color:var(--text-3);">Image tidak tersedia</div>'}
        <div class="ocr-field"><span class="ocr-label">Nama RS</span><input class="ocr-input" id="ocr-hospital" value="${window.currentSubmission.hospital_name || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Nama Pasien</span><input class="ocr-input" id="ocr-patient" value="${window.currentSubmission.patient_name || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">No. Kwitansi</span><input class="ocr-input" id="ocr-invoice" value="${window.currentSubmission.invoice_number || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Total Biaya</span><input class="ocr-input" id="ocr-cost" value="Rp ${window.currentSubmission.total_cost ? window.currentSubmission.total_cost.toLocaleString('id-ID') : '0'}"></div>
        <div class="ocr-field"><span class="ocr-label">Tanggal</span><input type="date" class="ocr-input" id="ocr-date" value="${window.currentSubmission.invoice_date || ''}"></div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <h3>Hasil OCR — Surat RS</h3>
        <span class="conf-bar"><span class="conf-track"><span class="conf-fill conf-mid" style="width:${sConfidence}%"></span></span><span class="conf-pct">${sConfidence}%</span></span>
      </div>
      <div class="card-body">
        ${suratImage ? `
          <div style="margin-bottom:12px;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;max-height:400px;display:flex;align-items:center;justify-content:center;background:#f5f5f5;">
            <img src="${suratImage}" style="max-width:100%;max-height:400px;width:auto;height:auto;object-fit:contain;display:block;"/>
          </div>
        ` : '<div style="padding:2rem;text-align:center;color:var(--text-3);">Image tidak tersedia</div>'}
        <div class="ocr-field"><span class="ocr-label">Nama Dokter</span><input class="ocr-input" id="ocr-doctor" value="${window.currentSubmission.doctor_name || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Diagnosa</span><input class="ocr-input" id="ocr-diagnosis" value="${window.currentSubmission.diagnosis || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Tanggal Mulai</span><input type="date" class="ocr-input" id="ocr-date-from" value="${window.currentSubmission.sick_date_from || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Tanggal Selesai</span><input type="date" class="ocr-input" id="ocr-date-to" value="${window.currentSubmission.sick_date_to || ''}"></div>
        <div class="ocr-field"><span class="ocr-label">Kategori</span>
          <select class="ocr-input" id="ocr-category" style="width:200px">
            <option ${window.currentSubmission.disease_category === 'Penyakit Infeksi' ? 'selected' : ''}>Penyakit Infeksi</option>
            <option ${window.currentSubmission.disease_category === 'Penyakit Kronis' ? 'selected' : ''}>Penyakit Kronis</option>
            <option ${window.currentSubmission.disease_category === 'Kecelakaan' ? 'selected' : ''}>Kecelakaan</option>
            <option ${window.currentSubmission.disease_category === 'Lainnya' ? 'selected' : ''}>Lainnya</option>
          </select>
        </div>
      </div>
    </div>
  </div>

  ${window.currentSubmission.is_duplicate ? `
  <div class="notif notif-warn mb-3">
    <span class="notif-icon">⚠</span>
    <div>
      <strong>Potensi duplikasi terdeteksi (${window.currentSubmission.duplicate_percentage || window.currentSubmission.similarity_score || 0}% kesamaan)!</strong><br>
      Ditemukan pengajuan serupa dengan ID: <strong>${window.currentSubmission.similar_submission_id || 'Unknown'}</strong>. Dokumen akan direview secara manual oleh Reviewer.
    </div>
  </div>
  ` : ''}

  <div class="flex gap-2" style="justify-content:flex-end">
    <button class="btn btn-ghost" onclick="goStep(1)">← Kembali</button>
    <button class="btn btn-primary" onclick="goStep(3)">Lanjut Konfirmasi →</button>
  </div>
  `;
}

function renderUploadStep3() {
  if (!window.currentSubmission) {
    return '<div class="notif notif-danger mb-3"><span class="notif-icon">✗</span><div>Data submission tidak ditemukan.</div></div>';
  }
  
  const kwitansiImage = window.currentSubmission.kwitansi_image || '';
  
  return `
  <div class="grid-2 mb-3">
    <div class="card">
      <div class="card-header"><h3>Ringkasan Pengajuan</h3></div>
      <div class="card-body">
        <div class="ocr-field"><span class="ocr-label">Nama Karyawan</span><span class="ocr-val">${window.currentSubmission.employee_name || '-'}</span></div>
        <div class="ocr-field"><span class="ocr-label">Nama RS</span><span class="ocr-val">${window.currentSubmission.hospital_name || '-'}</span></div>
        <div class="ocr-field"><span class="ocr-label">Diagnosa</span><span class="ocr-val">${window.currentSubmission.diagnosis || '-'}</span></div>
        <div class="ocr-field"><span class="ocr-label">Periode Sakit</span><span class="ocr-val">${window.currentSubmission.sick_date_from || '-'} – ${window.currentSubmission.sick_date_to || '-'}</span></div>
        <div class="ocr-field"><span class="ocr-label">Total Biaya</span><span class="ocr-val" style="color:var(--accent);font-weight:600">Rp ${window.currentSubmission.total_cost ? window.currentSubmission.total_cost.toLocaleString('id-ID') : '0'}</span></div>
        ${window.currentSubmission.is_duplicate ? `<div class="ocr-field"><span class="ocr-label">Status Duplikasi</span><span class="badge badge-dup">⚠ Flagged</span></div>` : ''}
      </div>
    </div>
    <div>
      <div class="card mb-2">
        <div class="card-header" style="background:var(--amber-light)"><h3 style="color:var(--amber)">🧾 Preview Kwitansi</h3></div>
        <div class="card-body">
          ${kwitansiImage ? `
            <div style="border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:12px;max-height:500px;display:flex;align-items:center;justify-content:center;background:#f5f5f5;">
              <img src="${kwitansiImage}" style="max-width:100%;max-height:500px;width:auto;height:auto;object-fit:contain;display:block;"/>
            </div>
          ` : ''}
          <div class="doc-mock">
            <div class="doc-mock-header">
              <div class="doc-mock-title">${(window.currentSubmission.hospital_name || 'RUMAH SAKIT').toUpperCase()}</div>
              <div class="doc-mock-sub">Kwitansi Resmi</div>
            </div>
            <div class="doc-mock-row"><span>Pasien</span><span>${window.currentSubmission.patient_name || '-'}</span></div>
            <div class="doc-mock-row"><span>Diagnosa</span><span>${window.currentSubmission.diagnosis || '-'}</span></div>
            <div class="doc-mock-row"><span>Tanggal</span><span>${window.currentSubmission.invoice_date || '-'}</span></div>
            <div class="doc-mock-row"><span style="font-weight:600">Total</span><span style="font-weight:600;color:var(--accent)">Rp ${window.currentSubmission.total_cost ? window.currentSubmission.total_cost.toLocaleString('id-ID') : '0'}</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="notif notif-info mb-3">
    <span class="notif-icon">ℹ</span>
    <div>Setelah dikirim, pengajuan akan masuk ke antrian Reviewer untuk diverifikasi. Anda akan mendapat notifikasi setelah dokumen disetujui.</div>
  </div>
  <div class="flex gap-2" style="justify-content:flex-end">
    <button class="btn btn-ghost" onclick="goStep(2)">← Kembali</button>
    <button class="btn btn-primary" onclick="confirmAndSubmit()">Kirim ke Reviewer ✓</button>
  </div>
  `;
}

// ════════════════════════════════════════════════
// GA — HISTORY
// ════════════════════════════════════════════════

async function renderGAHistory(el) {
  el.innerHTML = '<div class="page-header"><h2>Riwayat Pengajuan</h2><p>Memuat data...</p></div>';
  
  try {
    const mySubmissions = await loadMySubmissions();
    
    const statusMap = {
      uploaded: '<span class="badge badge-pending">Uploaded</span>',
      ocr_processing: '<span class="badge badge-pending">⏳ Proses OCR</span>',
      pending_review: '<span class="badge badge-pending">Menunggu Review</span>',
      duplicate_flagged: '<span class="badge badge-dup">⚠ Duplikat Terdeteksi</span>',
      approved: '<span class="badge badge-approved">✓ Disetujui</span>',
      rejected: '<span class="badge badge-rejected">✗ Ditolak</span>',
      completed: '<span class="badge badge-done">✓ Selesai</span>',
      stamped: '<span class="badge badge-stamp">Siap Kirim ke F&A</span>',
      pending_stamp: '<span class="badge badge-stamp">Menunggu Stempel</span>',
    };
    
    el.innerHTML = `
    <div class="page-header">
      <h2>Riwayat Pengajuan</h2>
      <p>Pantau status semua dokumen yang sudah Anda upload</p>
    </div>
    <div class="card">
      <div class="card-header">
        <h3>Semua Pengajuan (${mySubmissions.length})</h3>
        <div class="search-wrap"><input class="search-input" placeholder="Cari nama karyawan..."></div>
      </div>
      ${mySubmissions.length === 0 ? `
        <div class="card-body">
          <div class="empty-state">
            <div class="empty-icon">📋</div>
            <div class="empty-title">Belum ada pengajuan</div>
            <div class="empty-sub">Upload dokumen klaim medis untuk memulai</div>
          </div>
        </div>
      ` : `
        <div class="table-wrap">
          <table>
            <thead><tr>
              <th>ID</th><th>Nama Karyawan</th><th>Nama RS</th><th>Diagnosa</th><th>Biaya</th><th>Tanggal</th><th>Status</th><th>Aksi</th>
            </tr></thead>
            <tbody>
              ${mySubmissions.map(s=>`<tr>
                <td><span class="text-xs text-faint">${s.id}</span></td>
                <td class="font-medium">${s.employee}</td>
                <td class="text-sm text-muted">${s.rs}</td>
                <td class="text-sm">${s.diagnosis}</td>
                <td class="text-sm font-medium">${s.cost}</td>
                <td class="text-sm text-muted">${s.date}</td>
                <td>${statusMap[s.status]||s.status}</td>
                <td><button class="btn btn-ghost btn-sm" onclick="viewSubmissionDetail('${s.id}')">Detail</button></td>
              </tr>`).join('')}
            </tbody>
          </table>
        </div>
      `}
    </div>
    `;
  } catch (error) {
    el.innerHTML = `
      <div class="page-header">
        <h2>Riwayat Pengajuan</h2>
        <p>Gagal memuat data</p>
      </div>
      <div class="notif notif-danger">
        <span class="notif-icon">✗</span>
        <div>Error: ${error.message}</div>
      </div>
    `;
  }
}

async function viewSubmissionDetail(submissionId) {
  await loadSubmission(submissionId);
}

// ════════════════════════════════════════════════
// GA — STAMP & SEND
// ════════════════════════════════════════════════

function renderGAStamp(el) {
  el.innerHTML = '<div class="page-header"><h2>Stempel & Kirim ke F&A</h2><p>Dokumen yang sudah disetujui Reviewer</p></div><div class="card"><div class="card-body" style="text-align:center;padding:2rem;"><p>✅ Tidak ada dokumen menunggu stempel</p></div></div>';
}

// ════════════════════════════════════════════════
// REVIEWER — QUEUE
// ════════════════════════════════════════════════

function renderRVQueue(el) {
  el.innerHTML = '<div class="page-header"><h2>Antrian Review</h2><p>Dokumen yang menunggu verifikasi</p></div><div class="card"><div class="card-body" style="text-align:center;padding:2rem;"><p>📥 Tidak ada dokumen menunggu review</p></div></div>';
}

// ════════════════════════════════════════════════
// REVIEWER — HISTORY
// ════════════════════════════════════════════════

function renderRVHistory(el) {
  el.innerHTML = '<div class="page-header"><h2>Riwayat Review</h2><p>Dokumen yang sudah diverifikasi</p></div><div class="card"><div class="card-body" style="text-align:center;padding:2rem;"><p>📋 Riwayat review akan ditampilkan di sini</p></div></div>';
}

// ════════════════════════════════════════════════
// F&A — REPORT
// ════════════════════════════════════════════════

function renderFAReport(el) {
  el.innerHTML = '<div class="page-header"><h2>Laporan Klaim Medis</h2><p>Kwitansi yang siap untuk diproses pembayaran</p></div><div class="card"><div class="card-body" style="text-align:center;padding:2rem;"><p>📊 Laporan akan ditampilkan di sini</p></div></div>';
}

// ════════════════════════════════════════════════
// F&A — SUMMARY
// ════════════════════════════════════════════════

console.log('✓ dashboard.js loaded successfully');

function renderFASummary(el) {
  el.innerHTML = `
  <div class="page-header">
    <h2>Ringkasan & Analitik</h2>
    <p>Tren pengeluaran medis karyawan per periode</p>
  </div>

  <div class="grid-4 mb-4">
    <div class="stat-card">
      <div class="stat-value">Rp 14,2 jt</div>
      <div class="stat-label">Total YTD</div>
      <div class="stat-change">↑ 12% vs Thn lalu</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">Rp 120 jt</div>
      <div class="stat-label">Budget Tahunan</div>
      <div class="stat-change">Terpakai: 11.8%</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">6</div>
      <div class="stat-label">Total Klaim</div>
      <div class="stat-change">2 Pending</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">4.2</div>
      <div class="stat-label">Avg per Karyawan</div>
      <div class="stat-change">Rp 2.4 jt</div>
    </div>
  </div>

  <div class="grid-2 mb-4">
    <div class="card">
      <div class="card-header"><h3>📊 Biaya Klaim per Bulan (2025)</h3></div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(50px,1fr));gap:12px;align-items:flex-end;height:120px">
          ${[['Jan','35'],['Feb','42'],['Mar','28'],['Apr','58'],['Mei','45'],['Jun','67']].map(([m,v])=> `
          <div style="text-align:center">
            <div style="background:var(--accent);height:${v}%;border-radius:4px;margin-bottom:4px"></div>
            <div style="font-size:0.75rem;color:var(--text-2)">${m}</div>
          </div>
          `).join('')}
        </div>
        <div style="text-align:center;margin-top:12px;font-size:0.8rem;color:var(--text-3)">Skala: persentase dari tertinggi</div>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><h3>💊 Top Diagnosa Bulan Ini</h3></div>
      <div class="card-body">
        ${[ ['Demam Tifoid','Rp 1.250.000',78], ['Infeksi Saluran Napas','Rp 480.000',30], ['Gastritis Akut','Rp 730.000',46], ['Migrain Kronis','Rp 620.000',39], ['Hipertensi','Rp 215.000',14], ].map(([d,c,pct])=>`
        <div style="margin-bottom:14px">
          <div style="font-size:0.85rem;font-weight:500;margin-bottom:4px">${d}</div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <div style="flex:1;height:8px;background:var(--border);border-radius:4px;margin-right:10px;overflow:hidden">
              <div style="height:100%;background:var(--accent);width:${pct}%"></div>
            </div>
            <div style="font-size:0.8rem;color:var(--text-2);min-width:50px;text-align:right">${c}</div>
          </div>
        </div>
        `).join('')}
      </div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-header"><h3>🏥 Top RS</h3></div>
      <div class="card-body">
        ${[['RS Siloam Kebon Jeruk',4,'Rp 2.1 jt'],['RSUD Tarakan',2,'Rp 960rb'],['RS Pondok Indah',1,'Rp 730rb']].map(([n,c,t])=>`
        <div style="margin-bottom:16px">
          <div style="font-weight:500;font-size:0.9rem">${n}</div>
          <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:var(--text-2);margin-top:4px">
            <span>${c} klaim</span>
            <span style="font-weight:600;color:var(--accent)">${t}</span>
          </div>
        </div>
        `).join('')}
      </div>
    </div>
    <div class="card">
      <div class="card-header"><h3>👥 Biaya per Departemen</h3></div>
      <div class="card-body">
        ${[['Engineering','Rp 1.73 jt',68],['Marketing','Rp 480rb',19],['HR','Rp 215rb',8],['Finance','Rp 100rb',4]].map(([d,c,p])=>`
        <div style="margin-bottom:14px">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:0.9rem">
            <span style="font-weight:500">${d}</span>
            <span style="color:var(--text-2)">${c}</span>
          </div>
          <div style="height:8px;background:var(--border);border-radius:4px;overflow:hidden">
            <div style="height:100%;background:var(--accent);width:${p}%"></div>
          </div>
        </div>
        `).join('')}
      </div>
    </div>
  </div>
  `;
}
