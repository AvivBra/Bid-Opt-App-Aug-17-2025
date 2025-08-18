# איפיון מערכת עיצוב - Bid Optimizer

## 1. עקרונות עיצוב

### סגנון כללי
- **Minimalist** - עיצוב נקי ופשוט
- **Dark Mode** - רקע כהה לעבודה ממושכת
- **Centered Layout** - כל התוכן ממורכז
- **No Icons** - טקסט בלבד, ללא אייקונים או אימוג'ים
- **English UI** - כל הממשק באנגלית

### השראה
- Shadcn UI Design System
- Modern SaaS applications
- Focus on functionality over decoration

## 2. צבעים

### פלטת צבעים ראשית
```css
:root {
  --background: #0F0F0F;      /* שחור כהה */
  --card-bg: #1A1A1A;         /* אפור כהה מאוד */
  --border: #2D2D2D;          /* אפור כהה */
  --text-primary: #FFFFFF;     /* לבן */
  --text-secondary: #A1A1A1;   /* אפור בהיר */
  --accent: #8B5CF6;          /* ויולט */
  --accent-hover: #7C3AED;    /* ויולט כהה */
}
```

### צבעי סטטוס
```css
:root {
  --success: #10B981;         /* ירוק */
  --error: #EF4444;           /* אדום */
  --warning: #F59E0B;         /* כתום */
  --info: #3B82F6;            /* כחול */
  --pink-notice: #FFE4E1;     /* ורוד בהיר לשגיאות חישוב */
}
```

### שימוש בצבעים
| אלמנט | צבע רקע | צבע טקסט | גבול |
|-------|----------|-----------|-------|
| Background | #0F0F0F | - | - |
| Card | #1A1A1A | #FFFFFF | #2D2D2D |
| Button Primary | #8B5CF6 | #FFFFFF | - |
| Button Secondary | #2D2D2D | #FFFFFF | #2D2D2D |
| Input | #1A1A1A | #FFFFFF | #2D2D2D |
| Error Row | #FFE4E1 | #8B0000 | #FFB6C1 |

## 3. טיפוגרפיה

### פונט
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap');

body {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 14px;
  line-height: 1.5;
}
```

### היררכיית טקסט
| אלמנט | גודל | משקל | Case |
|-------|------|-------|------|
| Page Title | 28px | 400 | Title Case |
| Section Header | 18px | 400 | UPPERCASE |
| Body Text | 14px | 400 | Sentence case |
| Button Text | 14px | 400 | UPPERCASE |
| Label | 12px | 400 | Sentence case |
| Status | 12px | 400 | Sentence case |

## 4. Layout

### מבנה כללי
```css
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px;
}

.sidebar {
  width: 200px;
  position: fixed;
  height: 100vh;
  background: var(--card-bg);
  border-right: 1px solid var(--border);
}

.main-content {
  margin-left: 200px;
  padding: 40px;
}
```

### Spacing System
```css
/* Base unit: 8px */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

### Grid & Alignment
- כל התוכן ממורכז
- Cards עם padding של 32px
- רווח בין sections: 48px
- רווח בין elements: 16px

## 5. Components

### Buttons
```css
.button {
  height: 44px;
  width: 200px;
  padding: 0 24px;
  border-radius: 4px;
  font-size: 14px;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.button-primary {
  background: var(--accent);
  color: white;
}

.button-primary:hover {
  background: var(--accent-hover);
}

.button-secondary {
  background: var(--border);
  color: white;
  border: 1px solid var(--border);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Cards
```css
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 32px;
  margin-bottom: 24px;
}
```

### Forms
```css
.input {
  width: 100%;
  height: 40px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0 12px;
  color: white;
  font-size: 14px;
}

.checkbox {
  width: 16px;
  height: 16px;
  margin-right: 8px;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}
```

### Progress Bar
```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.3s ease;
}
```

### Alerts
```css
.alert {
  padding: 16px;
  border-radius: 4px;
  margin-bottom: 16px;
  border: 1px solid;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border-color: var(--success);
  color: var(--success);
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border-color: var(--error);
  color: var(--error);
}

.alert-info {
  background: rgba(59, 130, 246, 0.1);
  border-color: var(--info);
  color: var(--info);
}

.pink-notice {
  background: var(--pink-notice);
  border-color: #FFB6C1;
  color: #8B0000;
}
```

## 6. Animations

### Transitions
```css
/* Default transition */
* {
  transition: all 0.2s ease;
}

/* Progress animation */
@keyframes progress {
  from { width: 0; }
  to { width: 100%; }
}

/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide down */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Hover States
- Buttons: צבע כהה יותר
- Cards: הדגשת border
- Links: underline
- Checkboxes: הדגשת border

## 7. Responsive Design

### Breakpoints
```css
/* Desktop only - no mobile support */
@media (max-width: 1024px) {
  .mobile-warning {
    display: block;
    text-align: center;
    padding: 20px;
    background: var(--error);
    color: white;
  }
  
  .app-content {
    display: none;
  }
}
```

### Desktop Layout
- Min width: 1024px
- Max content width: 800px
- Sidebar: 200px fixed
- Main content: flexible

## 8. Accessibility

### Contrast Ratios
- Text on background: 15:1 (AAA)
- Buttons: 7:1 (AA)
- Borders: 3:1 (AA)

### Focus States
```css
*:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Keyboard Navigation
- Tab order logical
- All interactive elements accessible
- Skip links available
- Escape key closes modals

## 9. Dark Mode Specific

### מניעת עייפות עיניים
- רקע לא שחור מוחלט (#0F0F0F במקום #000000)
- טקסט לא לבן מוחלט לטקסט משני (#A1A1A1)
- קונטרסט מאוזן

### הדגשות
- שימוש בצבע accent (violet) להדגשות
- גבולות עדינים להפרדה
- רקע מעט בהיר יותר לcards

## 10. Implementation Notes

### Streamlit CSS Override
```python
def apply_custom_css():
    st.markdown("""
    <style>
        /* Custom CSS here */
        .stApp {
            background-color: #0F0F0F;
        }
        
        /* Override Streamlit defaults */
        .st-emotion-cache-* {
            font-family: 'Inter', sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)
```

### Component Classes
```python
# Button with custom class
st.markdown(
    '<button class="button button-primary">PROCESS FILES</button>',
    unsafe_allow_html=True
)

# Card container
st.markdown('<div class="card">', unsafe_allow_html=True)
# Content here
st.markdown('</div>', unsafe_allow_html=True)
```