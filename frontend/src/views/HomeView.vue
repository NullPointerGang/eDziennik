<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isAuthed = computed(() => auth.isAuthenticated)
const dashboardTarget = computed(() => (auth.role === 'student' ? { name: 'dashboard-student-home' } : { name: 'dashboard' }))
</script>

<template>
  <section class="landing">
    <div class="landing__bg" aria-hidden="true" />

    <div class="landing__container">
      <div class="landing__hero">
        <div class="landing__copy">
          <h1 class="landing__title">ePińczów — nowoczesny e‑dziennik</h1>
          <p class="landing__subtitle">
            Plany lekcji, oceny i komunikacja w jednym miejscu. Szybko, wygodnie i bezpiecznie
            dla uczniów i nauczycieli.
          </p>
          <div class="landing__cta">
            <RouterLink v-if="!isAuthed" class="btn btn--primary" to="/auth">Zaloguj się</RouterLink>
            <RouterLink v-else class="btn btn--success" :to="dashboardTarget">Przejdź do panelu</RouterLink>
            <!-- removed about link -->
          </div>
        </div>

        <div class="landing__preview">
          <div class="preview-card">
            <div class="preview-grid">
              <div class="tile tile--blue" />
              <div class="tile tile--emerald" />
              <div class="tile tile--violet" />
              <div class="tile tile--violet" />
              <div class="tile tile--blue" />
              <div class="tile tile--emerald" />
              <div class="tile tile--emerald" />
              <div class="tile tile--violet" />
              <div class="tile tile--blue" />
            </div>
          </div>
        </div>
      </div>

      <div class="landing__features">
        <h2 class="section-title">Dlaczego ePińczów?</h2>
        <div class="features">
          <div class="feature">
            <div class="feature__title feature__title--blue">Plan lekcji</div>
            <p class="feature__desc">Zawsze pod ręką, z uwzględnieniem zmian i zastępstw.</p>
          </div>
          <div class="feature">
            <div class="feature__title feature__title--emerald">Oceny</div>
            <p class="feature__desc">Przejrzysty obraz postępów i przydatne statystyki.</p>
          </div>
          <div class="feature">
            <div class="feature__title feature__title--violet">Komunikacja</div>
            <p class="feature__desc">Szybki kontakt z nauczycielami i klasami.</p>
          </div>
          <div class="feature">
            <div class="feature__title feature__title--pink">Bezpieczeństwo</div>
            <p class="feature__desc">Dostęp tylko dla uprawnionych użytkowników.</p>
          </div>
          <div class="feature">
            <div class="feature__title feature__title--amber">Szybkość</div>
            <p class="feature__desc">Lekki interfejs działający na każdym urządzeniu.</p>
          </div>
          <div class="feature">
            <div class="feature__title feature__title--cyan">Gotowy na integracje</div>
            <p class="feature__desc">Łatwe podłączenie backendu i zewnętrznych modułów.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
// Palette
$bg: #0f172a; // slate-900
$panel: rgba(17, 24, 39, 0.6); // glassy panel
$panel-border: rgba(148, 163, 184, 0.25);
$text: #e5e7eb; // slate-200
$muted: #94a3b8; // slate-400
$primary: #3b82f6; // blue-500
$success: #10b981; // emerald-500
$ghost: #111827; // slate-800

// Gradients
$g-hero: linear-gradient(180deg, rgba(2, 6, 23, 0) 0%, rgba(2, 6, 23, .6) 50%, #020617 100%);

.landing {
  position: relative;
  color: $text;
  background: $bg;

  &__bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: $g-hero;
  }

  &__container {
    position: relative;
    max-width: 1080px;
    margin: 0 auto;
    padding: 56px 16px 32px;
  }

  &__hero {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;

    @media (min-width: 768px) {
      grid-template-columns: 1.1fr 0.9fr;
      align-items: center;
      gap: 32px;
    }
  }

  &__copy {}

  &__title {
    margin: 0;
    font-size: 36px;
    line-height: 1.2;
    font-weight: 800;

    @media (min-width: 768px) { font-size: 48px; }
  }

  &__subtitle {
    margin-top: 12px;
    max-width: 58ch;
    color: $muted;
    font-size: 18px;
  }

  &__cta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 24px;
  }

  &__preview {
    .preview-card {
      border: 1px solid $panel-border;
      background: $panel;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,.3);

      .preview-grid {
        aspect-ratio: 16/9;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        padding: 6px;
        background: rgba(8, 15, 30, .6);
      }

      .tile {
        border-radius: 10px;
        &--blue { background: rgba(59, 130, 246, .35); }
        &--emerald { background: rgba(16, 185, 129, .35); }
        &--violet { background: rgba(139, 92, 246, .35); }
      }
    }
  }

  &__features {
    margin-top: 40px;

    .section-title {
      margin: 0 0 18px;
      font-size: 28px;
      font-weight: 700;
    }

    .features {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;

      @media (min-width: 640px) { grid-template-columns: repeat(2, 1fr); }
      @media (min-width: 1024px) { grid-template-columns: repeat(3, 1fr); }

      .feature {
        border: 1px solid $panel-border;
        background: $panel;
        border-radius: 14px;
        padding: 16px;
        transition: background .2s ease, transform .2s ease;

        &:hover { background: rgba(30, 41, 59, 0.6); transform: translateY(-2px); }

        &__title {
          font-weight: 600;
          &--blue { color: #60a5fa; }
          &--emerald { color: #34d399; }
          &--violet { color: #a78bfa; }
          &--pink { color: #f472b6; }
          &--amber { color: #fbbf24; }
          &--cyan { color: #22d3ee; }
        }

        &__desc { margin-top: 8px; color: $muted; }
      }
    }
  }
}

// Buttons
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid $panel-border;
  color: $text;
  background: #0b1220;
  cursor: pointer;
  text-decoration: none;
  transition: background .15s ease, border-color .15s ease, transform .06s ease;

  &:hover { background: #0d1424; }
  &:active { transform: translateY(1px); }

  &--primary {
    background: $primary; border-color: rgba(59, 130, 246, .6);
    &:hover { background: #60a5fa; }
  }
  &--success {
    background: $success; border-color: rgba(16, 185, 129, .6);
    &:hover { background: #34d399; }
  }
  &--ghost {
    background: transparent;
    &:hover { background: rgba(148,163,184,.08); }
  }
}
</style> 