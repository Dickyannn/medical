/**
 * MedClaim — Authentication Logic
 */

function doLogin() {
  const email = document.getElementById('login-email')?.value || '';
  const password = document.getElementById('login-pass')?.value || '';

  if (!email || !password) {
    alert('Email dan password harus diisi!');
    return;
  }

  // Demo authentication - in production, call backend API
  const demoAccounts = {
    'ga@perusahaan.id': { role: 'ga', password: 'password' },
    'reviewer@perusahaan.id': { role: 'reviewer', password: 'password' },
    'fa@perusahaan.id': { role: 'fa', password: 'password' },
  };

  const account = demoAccounts[email];
  if (account && account.password === password) {
    loginAs(account.role);
  } else {
    alert('Email atau password salah!');
  }
}

function loginAs(role) {
  localStorage.setItem('medclaim_role', role);
  
  // Redirect to appropriate dashboard
  const dashboardMap = {
    'ga': '/dashboard-ga.html',
    'reviewer': '/dashboard-reviewer.html',
    'fa': '/dashboard-fa.html'
  };
  
  window.location.href = dashboardMap[role] || '/login.html';
}
