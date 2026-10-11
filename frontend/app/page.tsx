// ─── CineVault — Главная страница каталога фильмов ───────────────────────────

// ──── Типы данных ────────────────────────────────────────────────────────────
interface Category {
  id: number;
  name: string;
  icon: string;
  count: number;
  color: string;
}

interface BackendMovie {
  id: number;
  title: string;
  description?: string | null;
  release_year?: number | null;
  rating?: number | null;
  category_id?: number | null;
}

interface BackendCategory {
  id: number;
  name: string;
  description?: string | null;
}

interface Movie {
  id: number;
  title: string;
  description: string;
  release_year: number;
  rating: number;
  category_id: number;
  category_name: string;
  poster_emoji: string;
}

//──── Backend API Host ──────────────────────────────────────────────────────────
const API_BASE_URL =
  process.env.INTERNAL_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

async function fetchCategoriesFromBackend(): Promise<Category[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/categories/`, {
      cache: "no-store", // Данные всегда свежие при обновлении страницы
    });

    if (!res.ok) {
      console.error("Ошибка ответа сервера:", res.status);
      return [];
    }

    const data: BackendCategory[] = await res.json();

    // Маппинг иконок и цветов для красивого UI
    const styleMap: Record<string, { icon: string; color: string }> = {
      "Боевики": { icon: "💥", color: "#e50914" },
      "Комедии": { icon: "😂", color: "#f5a623" },
      "Драмы": { icon: "🎭", color: "#7b61ff" },
      "Триллеры": { icon: "🔪", color: "#00c9a7" },
      "Ужасы": { icon: "👻", color: "#ff6b6b" },
      "Фантастика": { icon: "🚀", color: "#4fc3f7" },
      "Мелодрамы": { icon: "💕", color: "#f48fb1" },
      "Анимация": { icon: "🎨", color: "#69f0ae" },
    };

    return data.map((item) => {
      const visual = styleMap[item.name] || { icon: "🎬", color: "#6366f1" };
      return {
        id: item.id,
        name: item.name,
        icon: visual.icon,
        color: visual.color,
        count: 0,
      };
    });
  } catch (error) {
    console.error("Не удалось получить категории с бэкенда:", error);
    return [];
  }
}

// movies
async function fetchMoviesFromBackend(): Promise<BackendMovie[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/movies/`, {
      cache: "no-store", // Всегда свежие данные при перезагрузке
    });

    if (!res.ok) {
      console.error("Ошибка ответа сервера при загрузке фильмов:", res.status);
      return [];
    }

    return await res.json();
  } catch (error) {
    console.error("Не удалось получить фильмы с бэкенда:", error);
    return [];
  }
}


// Словарь эмодзи по умолчанию для постеров в зависимости от жанра
const GENRE_EMOJI_MAP: Record<string, string> = {
  "Боевики": "💥",
  "Комедии": "😂",
  "Драмы": "🎭",
  "Триллеры": "🔪",
  "Ужасы": "👻",
  "Фантастика": "🚀",
  "Мелодрамы": "💕",
  "Анимация": "🎨",
};

function enrichMovies(
  backendMovies: BackendMovie[],
  categories: Category[]
): Movie[] {
  // Быстрый поиск названия категории по id
  const categoryMap = new Map<number, string>();
  categories.forEach((cat) => categoryMap.set(cat.id, cat.name));

  return backendMovies.map((bm) => {
    const categoryName = (bm.category_id && categoryMap.get(bm.category_id)) || "Фильм";
    const posterEmoji = GENRE_EMOJI_MAP[categoryName] || "🎬";

    return {
      id: bm.id,
      title: bm.title,
      description: bm.description || "Описание фильма отсутствует.",
      release_year: bm.release_year || new Date().getFullYear(),
      rating: bm.rating ?? 0.0,
      category_id: bm.category_id || 0,
      category_name: categoryName,
      poster_emoji: posterEmoji,
    };
  });
}


// ──── Моковые данные ─────────────────────────────────────────────────────────
const CATEGORIES: Category[] = [
  { id: 1, name: "Боевики", icon: "💥", count: 124, color: "#e50914" },
  { id: 2, name: "Комедии", icon: "😂", count: 98, color: "#f5a623" },
  { id: 3, name: "Драмы", icon: "🎭", count: 215, color: "#7b61ff" },
  { id: 4, name: "Триллеры", icon: "🔪", count: 87, color: "#00c9a7" },
  { id: 5, name: "Ужасы", icon: "👻", count: 63, color: "#ff6b6b" },
  { id: 6, name: "Фантастика", icon: "🚀", count: 142, color: "#4fc3f7" },
  { id: 7, name: "Мелодрамы", icon: "💕", count: 76, color: "#f48fb1" },
  { id: 8, name: "Анимация", icon: "🎨", count: 51, color: "#69f0ae" },
];

const MOVIES: Movie[] = [
  { id: 1, title: "Интерстеллар", description: "Путешествие сквозь червоточину в поисках нового дома для человечества.", release_year: 2014, rating: 8.6, category_id: 6, category_name: "Фантастика", poster_emoji: "🌌" },
  { id: 2, title: "Крёстный отец", description: "История семьи Корлеоне — классика мирового кинематографа.", release_year: 1972, rating: 9.2, category_id: 3, category_name: "Драма", poster_emoji: "🌹" },
  { id: 3, title: "Тёмный рыцарь", description: "Бэтмен против Джокера в схватке за душу Готэм-сити.", release_year: 2008, rating: 9.0, category_id: 1, category_name: "Боевик", poster_emoji: "🦇" },
  { id: 4, title: "Паразиты", description: "Бедная семья проникает в жизнь богатой — острая социальная сатира.", release_year: 2019, rating: 8.5, category_id: 4, category_name: "Триллер", poster_emoji: "🏠" },
  { id: 5, title: "Волк с Уолл-стрит", description: "История головокружительного взлёта и падения брокера Джордана Белфорта.", release_year: 2013, rating: 8.2, category_id: 3, category_name: "Драма", poster_emoji: "💰" },
  { id: 6, title: "Начало", description: "Хакер сознания крадёт идеи из чужих снов. Реальность или иллюзия?", release_year: 2010, rating: 8.8, category_id: 6, category_name: "Фантастика", poster_emoji: "💫" },
  { id: 7, title: "Клуб бойцов", description: "Первое правило — не говори о клубе. Культовый фильм Финчера.", release_year: 1999, rating: 8.8, category_id: 4, category_name: "Триллер", poster_emoji: "🥊" },
  { id: 8, title: "Список Шиндлера", description: "Немецкий бизнесмен спасает евреев во время Холокоста.", release_year: 1993, rating: 9.0, category_id: 3, category_name: "Драма", poster_emoji: "📜" },
  { id: 9, title: "Безумный Макс: Дорога ярости", description: "Постапокалиптическое шоссе. Скорость, хаос, выживание.", release_year: 2015, rating: 8.1, category_id: 1, category_name: "Боевик", poster_emoji: "🔥" },
  { id: 10, title: "Унесённые призраками", description: "Девочка попадает в мир духов. Шедевр студии Ghibli.", release_year: 2001, rating: 8.6, category_id: 8, category_name: "Анимация", poster_emoji: "🐉" },
];

// ──── Star Rating ─────────────────────────────────────────────────────────────
function StarRating({ rating }: { rating: number }) {
  const stars = Math.round(rating / 2);
  return (
    <span style={{ color: "#f5c518", fontSize: "11px", letterSpacing: "1px" }}>
      {"★".repeat(stars)}{"☆".repeat(5 - stars)}
    </span>
  );
}

// ──── Category Card ───────────────────────────────────────────────────────────
function CategoryCard({ cat }: { cat: Category }) {
  return (
    <a
      href={`#cat-${cat.id}`}
      className="category-card"
      style={{ "--cat-color": cat.color } as React.CSSProperties}
      id={`category-card-${cat.id}`}
    >
      <div className="category-icon">{cat.icon}</div>
      <div>
        <div className="category-name">{cat.name}</div>
        <div className="category-count">{cat.count} фильмов</div>
      </div>
      <span className="category-arrow">→</span>
    </a>
  );
}

// ──── Movie Card ──────────────────────────────────────────────────────────────
function MovieCard({ movie }: { movie: Movie }) {
  return (
    <div className="movie-card" id={`movie-card-${movie.id}`}>
      <div className="movie-poster">
        <div className="poster-placeholder">
          <span>{movie.poster_emoji}</span>
          <span className="poster-placeholder-title">{movie.title}</span>
        </div>
        <div className="movie-poster-overlay">
          <div className="play-btn">▶</div>
        </div>
        <div className="movie-rating-badge">
          ★ {movie.rating.toFixed(1)}
        </div>
        <div className="movie-category-badge">{movie.category_name}</div>
      </div>
      <div className="movie-info">
        <div className="movie-title">{movie.title}</div>
        <div className="movie-meta">
          <StarRating rating={movie.rating} />
        </div>
        <div className="movie-meta">
          <span>{movie.release_year}</span>
          <span className="movie-meta-dot" />
          <span>{movie.rating} / 10</span>
        </div>
      </div>
    </div>
  );
}

// ──── Navbar ──────────────────────────────────────────────────────────────────
function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <a href="/" className="navbar-logo">
          <div className="logo-icon animate-pulse-glow">🎬</div>
          <span className="logo-text">Cine<span>Vault</span></span>
        </a>
        <ul className="navbar-nav">
          <li><a href="/" className="active">Главная</a></li>
          <li><a href="#genres">  Жанры</a></li>
          <li><a href="#movies">  Фильмы</a></li>
          <li><a href="#top">     Топ</a></li>
        </ul>
        <div className="navbar-search">
          <div className="search-input-wrap">
            <span className="search-icon">🔍</span>
            <input
              id="search-movies"
              type="search"
              className="search-input"
              placeholder="Найти фильм..."
            />
          </div>
        </div>
      </div>
    </nav>
  );
}

// ──── Hero ────────────────────────────────────────────────────────────────────
function Hero() {
  return (
    <section className="hero">
      <div className="hero-bg" />
      <div className="hero-grid" />
      <div className="hero-content">
        <div className="hero-badge animate-fade-in">
          <span>🎥</span> Новинки уже доступны
        </div>
        <h1 className="hero-title animate-fade-in-1">
          Ваш личный<br />
          <span className="highlight">кино-архив</span>
        </h1>
        <p className="hero-subtitle animate-fade-in-2">
          Более 800 фильмов по жанрам, рейтингам и годам выхода.
          Находите, изучайте и наслаждайтесь кино.
        </p>
        <div className="hero-actions animate-fade-in-3">
          <a href="#movies" className="btn btn-primary" id="hero-browse-btn">
            ▶ Смотреть каталог
          </a>
          <a href="#genres" className="btn btn-outline" id="hero-genres-btn">
            Жанры
          </a>
        </div>
        <div className="hero-stats animate-fade-in-3">
          <div className="stat-item">
            <span className="stat-value">800+</span>
            <span className="stat-label">Фильмов</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">8</span>
            <span className="stat-label">Жанров</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">9.2</span>
            <span className="stat-label">Макс. рейтинг</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">70+</span>
            <span className="stat-label">Лет истории</span>
          </div>
        </div>
      </div>
    </section>
  );
}

// ──── Page ────────────────────────────────────────────────────────────────────
export default async function Home() {
  // Параллельный запрос к бэкенду
  const [backendCategories, rawMovies] = await Promise.all([
    fetchCategoriesFromBackend(),
    fetchMoviesFromBackend(),
  ]);

  const categoriesBase = backendCategories.length > 0 ? backendCategories : CATEGORIES;

  // Обогащаем фильмы названиями категорий и постерами
  const moviesToDisplay = rawMovies.length > 0
    ? enrichMovies(rawMovies, categoriesBase)
    : MOVIES;

  // Динамический счетчик фильмов для категорий
  const countMap: Record<number, number> = {};
  moviesToDisplay.forEach((m) => {
    countMap[m.category_id] = (countMap[m.category_id] || 0) + 1;
  });

  const categoriesToDisplay = categoriesBase.map((c) => ({
    ...c,
    count: countMap[c.id] || c.count || 0,
  }));

  return (
    <>
      <Navbar />
      <main>
        <Hero />

        {/* Секция категорий с реальным количеством фильмов */}
        <section className="section" id="genres">
          <div className="section-header">
            <div>
              <h2 className="section-title">
                Жанры <span>&amp;</span> Категории
              </h2>
              <div className="divider" />
              <p className="section-subtitle">
                {backendCategories.length > 0
                  ? "Категории успешно загружены из базы данных бэкенда"
                  : "Выберите любимый жанр"}
              </p>
            </div>
            <a href="#genres" className="btn btn-ghost btn-sm" id="all-genres-btn">
              Все жанры ({categoriesToDisplay.length}) →
            </a>
          </div>

          <div className="categories-grid">
            {categoriesToDisplay.map((cat) => (
              <CategoryCard key={cat.id} cat={cat} />
            ))}
          </div>
        </section>

        {/* Секция фильмов из базы данных бэкенда */}
        <section className="section" id="movies" style={{ background: "var(--bg-secondary)" }}>
          <div className="section-header">
            <div>
              <h2 className="section-title">
                Популярные <span>фильмы</span>
              </h2>
              <div className="divider" />
              <p className="section-subtitle">
                {rawMovies.length > 0
                  ? `Показано фильмов из базы данных: ${moviesToDisplay.length}`
                  : "Лучшие по оценкам зрителей (демо-режим)"}
              </p>
            </div>
            <a href="#movies" className="btn btn-ghost btn-sm" id="all-movies-btn">
              Все фильмы ({moviesToDisplay.length}) →
            </a>
          </div>

          <div className="movies-grid">
            {moviesToDisplay.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-inner">
          <p className="footer-text">
            © 2026 <span className="footer-accent">CineVault</span> — Каталог фильмов
          </p>
          <p className="footer-text">
            Powered by <span className="footer-accent">FastAPI</span> + <span className="footer-accent">Next.js</span>
          </p>
        </div>
      </footer>
    </>
  );
}


