<template>
  <div class="landing">

    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-inner">
        <span class="nav-logo">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="8" fill="#4361ee"/>
            <path d="M7 10h14M7 14h10M7 18h12" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Boonya-Need-it
        </span>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </div>
        <div class="nav-actions">
          <DarkModeToggle />
          <button class="btn-ghost" @click="openModal('login')">Sign In</button>
          <button class="btn-primary" @click="openModal('register')">Get Started</button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <div class="badge">Supply Chain Management</div>
          <h1>Track every step.<br /><span class="accent">Deliver with confidence.</span></h1>
          <p class="hero-sub">
            Boonya-Need-it gives you real-time visibility into your supply chain —
            from suppliers to warehouses to final delivery — all in one place.
          </p>
          <div class="hero-ctas">
            <button class="btn-primary large" @click="openModal('register')">Get Started Free</button>
            <a href="#features" class="btn-outline large">See Features</a>
          </div>
        </div>

        <!-- App mockup -->
        <div class="hero-mockup">
          <div class="mockup-window">
            <div class="mockup-bar">
              <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
              <span class="mockup-title">Dashboard — Overview</span>
            </div>
            <div class="mockup-body">
              <div class="mock-sidebar">
                <div class="mock-nav-item active">Overview</div>
                <div class="mock-nav-item">Inventory</div>
                <div class="mock-nav-item">Orders</div>
                <div class="mock-nav-item">Suppliers</div>
                <div class="mock-nav-item">Reports</div>
              </div>
              <div class="mock-content">
                <div class="mock-stats">
                  <div class="mock-stat">
                    <div class="mock-stat-label">Total Orders</div>
                    <div class="mock-stat-value">1,284</div>
                    <div class="mock-stat-delta positive">+12.4%</div>
                  </div>
                  <div class="mock-stat">
                    <div class="mock-stat-label">In Transit</div>
                    <div class="mock-stat-value">348</div>
                    <div class="mock-stat-delta positive">+5.1%</div>
                  </div>
                  <div class="mock-stat">
                    <div class="mock-stat-label">Low Stock</div>
                    <div class="mock-stat-value">23</div>
                    <div class="mock-stat-delta negative">-3 items</div>
                  </div>
                </div>
                <div class="mock-chart">
                  <div class="mock-chart-label">Shipment Activity</div>
                  <div class="mock-bars">
                    <div class="mock-bar" style="height:40%"></div>
                    <div class="mock-bar" style="height:65%"></div>
                    <div class="mock-bar" style="height:50%"></div>
                    <div class="mock-bar" style="height:80%"></div>
                    <div class="mock-bar" style="height:55%"></div>
                    <div class="mock-bar" style="height:90%"></div>
                    <div class="mock-bar highlight" style="height:75%"></div>
                  </div>
                </div>
                <div class="mock-table">
                  <div class="mock-row header">
                    <span>Order ID</span><span>Supplier</span><span>Status</span>
                  </div>
                  <div class="mock-row">
                    <span>#ORD-4821</span><span>Acme Corp</span>
                    <span class="pill delivered">Delivered</span>
                  </div>
                  <div class="mock-row">
                    <span>#ORD-4820</span><span>GlobalParts</span>
                    <span class="pill transit">In Transit</span>
                  </div>
                  <div class="mock-row">
                    <span>#ORD-4819</span><span>SwiftMfg</span>
                    <span class="pill pending">Pending</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features" id="features">
      <div class="section-inner">
        <div class="section-label">Features</div>
        <h2>Everything you need to manage your supply chain</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon blue">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
              </svg>
            </div>
            <h3>Inventory Tracking</h3>
            <p>Monitor stock levels across multiple warehouses in real time. Get alerts before you run out.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon teal">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <h3>Order Management</h3>
            <p>Create, track, and manage purchase orders from placement to final delivery without the spreadsheets.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon indigo">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <h3>Supplier Directory</h3>
            <p>Maintain a centralized database of all your suppliers, contacts, and performance history.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon orange">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
            </div>
            <h3>Analytics & Reports</h3>
            <p>Understand lead times, costs, and fulfillment rates with dashboards built for operations teams.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon green">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <h3>Shipment Visibility</h3>
            <p>Track every shipment from dispatch to delivery. Know exactly where your goods are at all times.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon purple">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <h3>Secure & Reliable</h3>
            <p>JWT-based authentication and encrypted data storage keep your supply chain data safe.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="how-it-works" id="how-it-works">
      <div class="section-inner">
        <div class="section-label">How it works</div>
        <h2>Up and running in minutes</h2>
        <div class="steps">
          <div class="step">
            <div class="step-num">01</div>
            <h3>Create an account</h3>
            <p>Register with your email and set up your organization profile in under a minute.</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-num">02</div>
            <h3>Add your suppliers</h3>
            <p>Import or manually enter your supplier list, product catalog, and warehouse locations.</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-num">03</div>
            <h3>Start tracking</h3>
            <p>Create orders, monitor shipments, and get visibility across your entire supply chain.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="cta-banner">
      <div class="section-inner center">
        <h2>Ready to take control of your supply chain?</h2>
        <p>Join teams that rely on Boonya-Need-it to keep their operations running smoothly.</p>
        <button class="btn-primary large" @click="openModal('register')">Get Started Free</button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <span class="nav-logo">
          <svg width="20" height="20" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="8" fill="#4361ee"/>
            <path d="M7 10h14M7 14h10M7 18h12" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Boonya-Need-it
        </span>
        <span class="footer-copy">© 2026 Boonya-Need-it. ICCS225 Database Project.</span>
      </div>
    </footer>

    <!-- Modal Overlay -->
    <Transition name="fade">
      <div v-if="activeModal" class="overlay" @click.self="closeModal">
        <Transition name="slide-up">
          <div v-if="activeModal" class="modal">

            <!-- Close button -->
            <button class="modal-close" @click="closeModal" aria-label="Close">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>

            <!-- Logo -->
            <div class="modal-logo">
              <svg width="32" height="32" viewBox="0 0 28 28" fill="none">
                <rect width="28" height="28" rx="8" fill="#4361ee"/>
                <path d="M7 10h14M7 14h10M7 18h12" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Boonya-Need-it
            </div>

            <!-- LOGIN FORM -->
            <template v-if="activeModal === 'login'">
              <h2>Welcome back</h2>
              <p class="modal-sub">Sign in to your account</p>
              <form @submit.prevent="handleLogin">
                <div class="field">
                  <label>Username</label>
                  <input v-model="loginForm.username" type="text" placeholder="Enter username" required />
                </div>
                <div class="field">
                  <label>Password</label>
                  <input v-model="loginForm.password" type="password" placeholder="Enter password" required />
                </div>
                <p v-if="formError" class="form-error">{{ formError }}</p>
                <button type="submit" class="btn-submit" :disabled="loading">
                  {{ loading ? 'Signing in…' : 'Sign In' }}
                </button>
              </form>
              <p class="modal-switch">
                Don't have an account?
                <button class="link-btn" @click="switchModal('register')">Register</button>
              </p>
            </template>

            <!-- REGISTER FORM -->
            <template v-else-if="activeModal === 'register'">
              <h2>Create account</h2>
              <p class="modal-sub">Get started for free</p>
              <form @submit.prevent="handleRegister">
                <div class="field">
                  <label>Username</label>
                  <input v-model="registerForm.username" type="text" placeholder="Choose a username" required />
                </div>
                <div class="field">
                  <label>Email</label>
                  <input v-model="registerForm.email" type="email" placeholder="Enter your email" required />
                </div>
                <div class="field">
                  <label>Password</label>
                  <input v-model="registerForm.password" type="password" placeholder="Create a password" required />
                </div>
                <p v-if="formError" class="form-error">{{ formError }}</p>
                <p v-if="formSuccess" class="form-success">{{ formSuccess }}</p>
                <button type="submit" class="btn-submit" :disabled="loading">
                  {{ loading ? 'Registering…' : 'Create Account' }}
                </button>
              </form>
              <p class="modal-switch">
                Already have an account?
                <button class="link-btn" @click="switchModal('login')">Sign In</button>
              </p>
            </template>

          </div>
        </Transition>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../api/auth'
import DarkModeToggle from '../components/DarkModeToggle.vue'

const router = useRouter()

const activeModal = ref(null)
const loading = ref(false)
const formError = ref('')
const formSuccess = ref('')

const loginForm = ref({ username: '', password: '' })
const registerForm = ref({ username: '', email: '', password: '' })

function openModal(type) {
  activeModal.value = type
  formError.value = ''
  formSuccess.value = ''
}

function closeModal() {
  activeModal.value = null
  formError.value = ''
  formSuccess.value = ''
}

function switchModal(type) {
  formError.value = ''
  formSuccess.value = ''
  activeModal.value = type
}

async function handleLogin() {
  formError.value = ''
  loading.value = true
  try {
    await login(loginForm.value.username, loginForm.value.password)
    router.push('/dashboard')
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  formError.value = ''
  formSuccess.value = ''
  loading.value = true
  try {
    await register(registerForm.value.username, registerForm.value.email, registerForm.value.password)
    formSuccess.value = 'Account created! Switching to sign in…'
    setTimeout(() => switchModal('login'), 1400)
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
* { box-sizing: border-box; }

.landing {
  font-family: 'Inter', 'Segoe UI', sans-serif;
  color: var(--color-text);
  background: var(--color-bg);
}

/* ── Navbar ── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-navbar-bg);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border-subtle);
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 2rem;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-text);
  text-decoration: none;
  flex-shrink: 0;
}
.nav-links {
  display: flex;
  gap: 1.75rem;
  flex: 1;
}
.nav-links a {
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a:hover { color: var(--color-primary); }
.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* ── Buttons ── */
.btn-ghost {
  background: none;
  border: none;
  padding: 0.45rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  font-family: inherit;
}
.btn-ghost:hover { background: var(--color-surface-hover); }

.btn-primary {
  text-decoration: none;
  padding: 0.5rem 1.1rem;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  display: inline-block;
  font-family: inherit;
}
.btn-primary:hover { background: var(--color-primary-hover); transform: translateY(-1px); }
.btn-primary.large { padding: 0.75rem 1.75rem; font-size: 1rem; border-radius: 10px; }

.btn-outline {
  text-decoration: none;
  padding: 0.75rem 1.75rem;
  border: 2px solid var(--color-border);
  color: var(--color-text);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  transition: border-color 0.2s, color 0.2s;
  display: inline-block;
}
.btn-outline:hover { border-color: var(--color-primary); color: var(--color-primary); }

/* ── Hero ── */
.hero {
  background: linear-gradient(160deg, var(--hero-grad-1) 0%, var(--hero-grad-2) 50%, var(--hero-grad-3) 100%);
  padding: 5rem 2rem 0;
  overflow: hidden;
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  gap: 4rem;
}
.hero-text {
  flex: 1;
  padding-top: 2rem;
  padding-bottom: 4rem;
  min-width: 340px;
}
.badge {
  display: inline-block;
  background: var(--color-primary-tint);
  color: var(--color-primary);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.35rem 0.9rem;
  border-radius: 100px;
  margin-bottom: 1.25rem;
}
.hero-text h1 {
  font-size: 3rem;
  line-height: 1.18;
  font-weight: 800;
  margin: 0 0 1.25rem;
  color: var(--color-text);
}
.accent { color: var(--color-primary); }
.hero-sub {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--color-text-muted);
  max-width: 440px;
  margin-bottom: 2rem;
}
.hero-ctas { display: flex; gap: 1rem; flex-wrap: wrap; }

/* ── Mockup ── */
.hero-mockup {
  flex: 1.1;
  min-width: 320px;
  display: flex;
  align-items: flex-end;
}
.mockup-window {
  width: 100%;
  background: #fff;
  border-radius: 14px 14px 0 0;
  box-shadow: 0 8px 40px rgba(67,97,238,0.15), 0 2px 8px rgba(0,0,0,0.06);
  overflow: hidden;
  border: 1px solid #e4e8f5;
  border-bottom: none;
}
.mockup-bar {
  background: #f7f8fc;
  border-bottom: 1px solid #eaecf4;
  padding: 0.6rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.red    { background: #ff5f57; }
.dot.yellow { background: #ffbd2e; }
.dot.green  { background: #28c840; }
.mockup-title { margin-left: 0.5rem; font-size: 0.72rem; color: #888; font-weight: 500; }
.mockup-body { display: flex; height: 320px; }
.mock-sidebar {
  width: 110px;
  background: #f9fafb;
  border-right: 1px solid #eaecf4;
  padding: 0.75rem 0;
  flex-shrink: 0;
}
.mock-nav-item { padding: 0.45rem 0.85rem; font-size: 0.72rem; color: #888; border-radius: 6px; margin: 2px 6px; cursor: default; }
.mock-nav-item.active { background: #eef0fc; color: #4361ee; font-weight: 600; }
.mock-content { flex: 1; padding: 0.75rem 1rem; overflow: hidden; display: flex; flex-direction: column; gap: 0.65rem; }
.mock-stats { display: flex; gap: 0.5rem; }
.mock-stat { flex: 1; background: #f5f7ff; border-radius: 8px; padding: 0.5rem 0.65rem; border: 1px solid #e8ecff; }
.mock-stat-label { font-size: 0.62rem; color: #888; }
.mock-stat-value { font-size: 1rem; font-weight: 700; color: #1a1a2e; margin: 2px 0; }
.mock-stat-delta { font-size: 0.6rem; font-weight: 600; }
.mock-stat-delta.positive { color: #2a9d8f; }
.mock-stat-delta.negative { color: #e63946; }
.mock-chart { background: #f9fafb; border-radius: 8px; padding: 0.5rem 0.65rem; border: 1px solid #eee; }
.mock-chart-label { font-size: 0.62rem; color: #888; margin-bottom: 0.4rem; }
.mock-bars { display: flex; align-items: flex-end; gap: 4px; height: 50px; }
.mock-bar { flex: 1; background: #d0d8f8; border-radius: 3px 3px 0 0; }
.mock-bar.highlight { background: #4361ee; }
.mock-table { font-size: 0.65rem; }
.mock-row { display: flex; gap: 0.5rem; padding: 0.3rem 0; border-bottom: 1px solid #f0f0f0; align-items: center; }
.mock-row.header { color: #aaa; font-weight: 600; }
.mock-row span { flex: 1; color: #444; }
.pill { font-size: 0.58rem; font-weight: 700; padding: 2px 6px; border-radius: 100px; }
.pill.delivered { background: #d4f7f0; color: #2a9d8f; }
.pill.transit   { background: #e8ecff; color: #4361ee; }
.pill.pending   { background: #fff3cd; color: #b97800; }

/* ── Sections ── */
.section-inner { max-width: 1200px; margin: 0 auto; padding: 5rem 2rem; }
.section-label { font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-primary); margin-bottom: 0.75rem; }
.features h2, .how-it-works h2, .cta-banner h2 { font-size: 2rem; font-weight: 800; margin: 0 0 2.5rem; }
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.feature-card { padding: 1.75rem; border: 1px solid var(--color-border-subtle); border-radius: 14px; transition: box-shadow 0.2s, transform 0.2s; }
.feature-card:hover { box-shadow: 0 8px 24px rgba(67,97,238,0.1); transform: translateY(-2px); }
.feature-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; }
.feature-icon.blue   { background: #e8ecff; color: #4361ee; }
.feature-icon.teal   { background: #d4f7f0; color: #2a9d8f; }
.feature-icon.indigo { background: #ede9ff; color: #7c3aed; }
.feature-icon.orange { background: #fff0e0; color: #e07b00; }
.feature-icon.green  { background: #e0f5e9; color: #1e8a4a; }
.feature-icon.purple { background: #f3e8ff; color: #9333ea; }
.feature-card h3 { font-size: 1rem; font-weight: 700; margin: 0 0 0.5rem; }
.feature-card p  { font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin: 0; }

/* ── How it works ── */
.how-it-works { background: var(--color-bg-alt); }
.steps { display: flex; align-items: flex-start; gap: 1rem; }
.step { flex: 1; background: var(--color-surface); border-radius: 14px; padding: 1.75rem; border: 1px solid var(--color-border-subtle); }
.step-arrow { font-size: 1.5rem; color: var(--color-border); padding-top: 1.75rem; flex-shrink: 0; }
.step-num { font-size: 2rem; font-weight: 800; color: var(--color-primary-tint); margin-bottom: 0.75rem; line-height: 1; }
.step h3 { font-size: 1rem; font-weight: 700; margin: 0 0 0.5rem; }
.step p  { font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin: 0; }

/* ── CTA Banner ── */
.cta-banner { background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%); color: #fff; }
.cta-banner .section-inner.center { text-align: center; }
.cta-banner h2 { color: #fff; margin-bottom: 0.75rem; }
.cta-banner p  { color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 2rem; }
.cta-banner .btn-primary { background: #fff; color: #4361ee; }
.cta-banner .btn-primary:hover { background: #eef0fc; transform: none; }

/* ── Footer ── */
.footer { border-top: 1px solid var(--color-border-subtle); padding: 1.5rem 2rem; }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
.footer-copy { font-size: 0.82rem; color: var(--color-text-subtle); }

/* ── Modal Overlay ── */
.overlay {
  position: fixed;
  inset: 0;
  background: var(--color-overlay);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal {
  background: var(--color-surface);
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  position: relative;
  box-shadow: var(--shadow-lg);
}

.modal-close {
  position: absolute;
  top: 1.1rem;
  right: 1.1rem;
  background: var(--color-surface-hover);
  border: none;
  border-radius: 8px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-muted);
  transition: background 0.15s, color 0.15s;
}
.modal-close:hover { background: var(--color-border); color: var(--color-text); }

.modal-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 1rem;
  color: var(--color-text);
  margin-bottom: 1.5rem;
}

.modal h2 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--color-text);
  margin: 0 0 0.25rem;
}
.modal-sub {
  font-size: 0.88rem;
  color: var(--color-text-subtle);
  margin-bottom: 1.5rem;
}

.field { margin-bottom: 1rem; }
label { display: block; font-size: 0.82rem; font-weight: 600; color: var(--color-text); margin-bottom: 0.4rem; }
input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: 9px;
  font-size: 0.95rem;
  box-sizing: border-box;
  font-family: inherit;
  background: var(--color-surface);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}
input:focus { border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(67,97,238,0.12); }

.btn-submit {
  width: 100%;
  padding: 0.78rem;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 0.5rem;
  font-family: inherit;
  transition: background 0.2s, transform 0.1s;
}
.btn-submit:hover:not(:disabled) { background: var(--color-primary-hover); transform: translateY(-1px); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.form-error   { color: var(--color-danger); font-size: 0.82rem; margin: 0.4rem 0; }
.form-success { color: var(--color-success); font-size: 0.82rem; margin: 0.4rem 0; }

.modal-switch {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.88rem;
  color: var(--color-text-subtle);
}
.link-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 700;
  font-size: inherit;
  cursor: pointer;
  padding: 0;
  font-family: inherit;
}
.link-btn:hover { text-decoration: underline; }

/* ── Transitions ── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active { transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.22s ease; }
.slide-up-leave-active { transition: transform 0.2s ease, opacity 0.2s ease; }
.slide-up-enter-from  { transform: translateY(24px) scale(0.97); opacity: 0; }
.slide-up-leave-to    { transform: translateY(12px) scale(0.97); opacity: 0; }
</style>
