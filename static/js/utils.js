/**
 * Utilitas JavaScript bersama yang dipakai lintas halaman
 * (Projects, Experience, dst.). Dimuat dari base.html.
 */

/**
 * Mengubah karakter khusus HTML menjadi entity agar data dari server/JSON
 * ditampilkan sebagai teks biasa, bukan diperlakukan sebagai kode HTML.
 * Wajib dipakai pada setiap nilai yang disisipkan ke innerHTML (mencegah XSS).
 */
function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

/**
 * Membaca nilai cookie berdasarkan namanya. Dipakai untuk mengambil token
 * CSRF (cookie "csrftoken") yang dikirim lewat header X-CSRFToken.
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
