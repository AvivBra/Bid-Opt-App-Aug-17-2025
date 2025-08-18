# איפיון פריסת UI - Bid Optimizer

## 1. מבנה כללי

### Layout Structure
```
┌────────────────────────────────────────────────────┐
│                    Header (Optional)                │
├────────┬───────────────────────────────────────────┤
│        │                                           │
│  Side  │           Main Content Area               │
│  Bar   │         (Centered Container)              │
│ (200px)│            (max: 800px)                   │
│        │                                           │
└────────┴───────────────────────────────────────────┘
```

### Dimensions
```css
:root {
  --sidebar-width: 200px;
  --content-max-width: 800px;
  --header-height: 0px;  /* No header currently */
  --spacing-unit: 8px;
}
```

## 2. Grid System

### Main Grid
```css
.app-container {
  display: grid;
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-rows: 1fr;
  min-height: 100vh;
  background: #0F0F0F;
}

.main-content {
  display: flex;
  justify-content: center;
  padding: 40px 24px;
}

.content-container {
  width: 100%;
  max-width: var(--content-max-width);
}
```

### Section Grid
```css
.section {
  background: #1A1A1A;
  border: 1px solid #2D2D2D;
  border-radius: 4px;
  padding: 32px;
  margin-bottom: 48px;
}

.section-header {
  font-size: 18px;
  font-weight: 400;
  text-transform: uppercase;
  margin-bottom: 24px;
  color: #FFFFFF;
}
```

## 3. Component Layout

### Upload Section
```
┌──────────────────────────────────────┐
│         SELECT OPTIMIZATIONS         │
│ ┌──────────────────────────────────┐ │
│ │ □ Zero Sales                     │ │
│ │ □ Future Optimization (TBD)      │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│           UPLOAD FILES               │
│                                      │
│  ┌─────────────┐ ┌─────────────┐   │
│  │Download     │ │ Bulk 7 Days │   │
│  │Template     │ │             │   │
│  └─────────────┘ └─────────────┘   │
│                                      │
│  ┌─────────────┐ ┌─────────────┐   │
│  │Bulk 30 Days │ │Bulk 60 Days │   │
│  └─────────────┘ └─────────────┘   │
│                                      │
│       ┌─────────────┐               │
│       │  Data Rova  │               │
│       └─────────────┘               │
│                                      │
│  Status: Template ✓ | Bulk 30 ✓     │
└──────────────────────────────────────┘
```

### Validation Section
```
┌──────────────────────────────────────┐
│         DATA VALIDATION              │
│                                      │
│  All portfolios valid                │
│  234 rows ready for processing       │
│                                      │
│       ┌─────────────┐               │
│       │Process Files│               │
│       └─────────────┘               │
└──────────────────────────────────────┘
```

### Output Section
```
┌──────────────────────────────────────┐
│          OUTPUT FILES                │
│                                      │
│  Processing complete                 │
│  Working: 2.4MB | Clean: 1.8MB      │
│                                      │
│  ┌─────────────┐ ┌─────────────┐   │
│  │  Download   │ │  Download   │   │
│  │  Working    │ │   Clean     │   │
│  └─────────────┘ └─────────────┘   │
│                                      │
│       ┌─────────────┐               │
│       │    Reset    │               │
│       └─────────────┘               │
└──────────────────────────────────────┘
```

## 4. Spacing System

### Vertical Spacing
```css
.spacing-xs { margin-bottom: 4px; }
.spacing-sm { margin-bottom: 8px; }
.spacing-md { margin-bottom: 16px; }
.spacing-lg { margin-bottom: 24px; }
.spacing-xl { margin-bottom: 32px; }
.spacing-2xl { margin-bottom: 48px; }
.spacing-3xl { margin-bottom: 64px; }
```

### Horizontal Spacing
```css
.gap-xs { gap: 4px; }
.gap-sm { gap: 8px; }
.gap-md { gap: 16px; }
.gap-lg { gap: 24px; }
.gap-xl { gap: 32px; }
```

## 5. Button Layout

### Button Grid
```css
.button-grid-2x2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.button-grid-1x1 {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.button {
  width: 200px;
  height: 44px;
  margin: 0 auto;
}
```

### Button Arrangements
```
Two columns:
┌─────────┐ ┌─────────┐
│ Button1 │ │ Button2 │
└─────────┘ └─────────┘

Single centered:
     ┌─────────┐
     │ Button  │
     └─────────┘
```

## 6. Form Layout

### Checkbox List
```css
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: #0F0F0F;
  border: 1px solid #2D2D2D;
  border-radius: 4px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox {
  width: 16px;
  height: 16px;
}
```

## 7. Progress Layout

### Progress Bar
```css
.progress-container {
  width: 100%;
  margin: 24px 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #2D2D2D;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #8B5CF6;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  margin-top: 8px;
  font-size: 12px;
  color: #A1A1A1;
}
```

## 8. Message Layout

### Alert Box
```css
.alert {
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 4px;
  border: 1px solid;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border-color: #EF4444;
  color: #EF4444;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10B981;
  color: #10B981;
}

.pink-notice {
  background: #FFE4E1;
  border-color: #FFB6C1;
  color: #8B0000;
  padding: 20px;
  text-align: center;
  margin: 20px 0;
}
```

## 9. Responsive Layout

### Breakpoints
```css
/* Desktop only - minimum 1024px */
@media (min-width: 1024px) {
  .app-container {
    display: grid;
  }
}

/* Tablet and Mobile - Not supported */
@media (max-width: 1023px) {
  .app-container {
    display: none;
  }
  
  .mobile-warning {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    text-align: center;
    padding: 20px;
  }
  
  .mobile-warning::after {
    content: "Please use a desktop browser to access this application.";
    font-size: 18px;
    color: #FFFFFF;
  }
}
```

## 10. Flex Utilities

### Flexbox Classes
```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }
.flex-center { justify-content: center; align-items: center; }
.flex-between { justify-content: space-between; }
.flex-start { justify-content: flex-start; }
.flex-end { justify-content: flex-end; }
.flex-wrap { flex-wrap: wrap; }
.flex-1 { flex: 1; }
```

## 11. Z-Index Layers

### Layer System
```css
:root {
  --z-base: 0;
  --z-dropdown: 100;
  --z-sidebar: 200;
  --z-modal: 300;
  --z-tooltip: 400;
  --z-notification: 500;
}
```

## 12. Streamlit Overrides

### Custom Streamlit Layout
```python
def apply_custom_layout():
    """Apply custom layout to Streamlit"""
    
    st.markdown("""
    <style>
    /* Remove default padding */
    .stApp {
        background: #0F0F0F;
    }
    
    /* Custom container */
    .main .block-container {
        max-width: 800px;
        padding: 40px 24px;
        margin: 0 auto;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom sections */
    .section-container {
        background: #1A1A1A;
        border: 1px solid #2D2D2D;
        border-radius: 4px;
        padding: 32px;
        margin-bottom: 48px;
    }
    
    /* Center all buttons */
    .stButton > button {
        width: 200px;
        height: 44px;
        margin: 0 auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
```

## 13. Layout Components

### Section Component
```python
def render_section(title: str, content):
    """Render a section with consistent styling"""
    
    st.markdown(
        f"""
        <div class="section-container">
            <h2 class="section-header">{title}</h2>
        """,
        unsafe_allow_html=True
    )
    
    content()  # Render content
    
    st.markdown("</div>", unsafe_allow_html=True)
```

### Button Row Component
```python
def render_button_row(buttons: list, columns: int = 2):
    """Render buttons in a row"""
    
    if columns == 1:
        for btn in buttons:
            st.button(btn['label'], key=btn['key'])
    else:
        cols = st.columns(columns)
        for i, btn in enumerate(buttons):
            with cols[i % columns]:
                st.button(btn['label'], key=btn['key'])
```

## 14. Empty States

### No Files Uploaded
```
┌──────────────────────────────────────┐
│           UPLOAD FILES               │
│                                      │
│         No files uploaded            │
│                                      │
│    Upload files to get started       │
│                                      │
└──────────────────────────────────────┘
```

### No Optimizations Selected
```
┌──────────────────────────────────────┐
│       SELECT OPTIMIZATIONS           │
│                                      │
│   No optimizations selected          │
│                                      │
│  Select at least one optimization    │
│                                      │
└──────────────────────────────────────┘
```