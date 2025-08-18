# איפיון נביגציה - Bid Optimizer

## 1. סקירה כללית

### מבנה הנביגציה
- Sidebar קבוע בצד שמאל
- 2 עמודים ראשיים
- נביגציה פשוטה בלחיצה
- שמירת state בין מעברים

## 2. Sidebar

### מבנה
```
┌──────────────┐
│              │
│     BID      │ ← Active (Violet)
│  OPTIMIZER   │   
│              │
│──────────────│
│              │
│  CAMPAIGNS   │ ← Inactive (Gray)
│  OPTIMIZER   │   Disabled in Phase 1
│              │
└──────────────┘
```

### עיצוב
```css
.sidebar {
  width: 200px;
  height: 100vh;
  background: #1A1A1A;
  border-right: 1px solid #2D2D2D;
  position: fixed;
  left: 0;
  top: 0;
}

.sidebar-item {
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 1px solid #2D2D2D;
}

.sidebar-item.active {
  background: #8B5CF6;
  color: white;
}

.sidebar-item.inactive {
  background: transparent;
  color: #A1A1A1;
}

.sidebar-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## 3. Pages Structure

### Available Pages
```python
PAGES = {
    'bid_optimizer': {
        'title': 'BID OPTIMIZER',
        'enabled': True,
        'component': bid_optimizer_page,
        'icon': None  # No icons
    },
    'campaigns_optimizer': {
        'title': 'CAMPAIGNS OPTIMIZER',
        'enabled': False,  # Phase 1
        'component': campaigns_optimizer_page,  # TBD
        'icon': None
    }
}
```

## 4. Navigation Logic

### Page Selection
```python
def handle_navigation():
    """Main navigation handler"""
    
    # Create sidebar
    with st.sidebar:
        st.markdown(
            """
            <style>
            .sidebar-nav {
                padding: 0;
                margin: 0;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Bid Optimizer button
        if st.button(
            "BID OPTIMIZER",
            key="nav_bid",
            use_container_width=True,
            disabled=False
        ):
            st.session_state.current_page = 'bid_optimizer'
            clear_page_messages()
        
        # Campaigns Optimizer button (disabled in Phase 1)
        if st.button(
            "CAMPAIGNS OPTIMIZER",
            key="nav_campaigns",
            use_container_width=True,
            disabled=True  # Enabled in Phase 5
        ):
            st.session_state.current_page = 'campaigns_optimizer'
            clear_page_messages()
    
    # Render current page
    render_current_page()
```

### Page Rendering
```python
def render_current_page():
    """Render the currently selected page"""
    
    current = st.session_state.get('current_page', 'bid_optimizer')
    
    if current == 'bid_optimizer':
        render_bid_optimizer_page()
    elif current == 'campaigns_optimizer':
        render_campaigns_optimizer_page()  # TBD
    else:
        st.error("Page not found")
```

## 5. State Management During Navigation

### Preserving State
```python
def switch_page(new_page: str):
    """Switch to a new page while preserving state"""
    
    # Save current page state
    save_current_page_state()
    
    # Update current page
    st.session_state.current_page = new_page
    
    # Load new page state
    load_page_state(new_page)
    
    # Clear temporary UI elements
    clear_temporary_ui()
    
    # Rerun to render new page
    st.experimental_rerun()
```

### Page-Specific State
```python
def save_current_page_state():
    """Save state of current page before switching"""
    
    current = st.session_state.current_page
    
    if current == 'bid_optimizer':
        # Save bid optimizer specific state
        st.session_state.bid_state = {
            'selected_optimizations': st.session_state.get('selected_optimizations', []),
            'uploaded_files': get_uploaded_files_list(),
            'processing_status': st.session_state.get('processing_status', 'idle')
        }
    
    elif current == 'campaigns_optimizer':
        # TBD - Save campaigns state
        pass
```

## 6. URL Routing (Optional Enhancement)

### Query Parameters
```python
def setup_url_routing():
    """Setup URL-based routing"""
    
    # Get query params
    params = st.experimental_get_query_params()
    page = params.get('page', ['bid_optimizer'])[0]
    
    # Validate and set page
    if page in PAGES and PAGES[page]['enabled']:
        st.session_state.current_page = page
    
    # Update URL when page changes
    st.experimental_set_query_params(
        page=st.session_state.current_page
    )
```

## 7. Navigation Guards

### Preventing Navigation
```python
def can_leave_page() -> bool:
    """Check if user can leave current page"""
    
    # Check if processing is in progress
    if st.session_state.get('processing_status') == 'processing':
        st.warning("Processing in progress. Please wait...")
        return False
    
    # Check for unsaved changes
    if has_unsaved_changes():
        response = st.warning("You have unsaved changes. Continue?")
        return response
    
    return True
```

### Navigation Confirmation
```python
def confirm_navigation(target_page: str):
    """Confirm navigation when there are unsaved changes"""
    
    if st.session_state.get('has_output_files'):
        with st.modal("Confirm Navigation"):
            st.write("You have generated files that haven't been downloaded.")
            st.write("They will be lost if you navigate away.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Stay on Page"):
                    return False
            with col2:
                if st.button("Leave Page"):
                    return True
    
    return True
```

## 8. Breadcrumbs (Optional)

### Breadcrumb Display
```python
def render_breadcrumbs():
    """Render breadcrumb navigation"""
    
    current = st.session_state.current_page
    
    breadcrumbs = []
    if current == 'bid_optimizer':
        breadcrumbs = ["Home", "Bid Optimizer"]
    elif current == 'campaigns_optimizer':
        breadcrumbs = ["Home", "Campaigns Optimizer"]
    
    st.markdown(
        " > ".join(breadcrumbs),
        unsafe_allow_html=True
    )
```

## 9. Keyboard Navigation (Enhancement)

### Keyboard Shortcuts
```python
def setup_keyboard_navigation():
    """Setup keyboard shortcuts for navigation"""
    
    # Register keyboard event listeners
    st.components.v1.html(
        """
        <script>
        document.addEventListener('keydown', function(e) {
            // Alt + 1: Bid Optimizer
            if (e.altKey && e.key === '1') {
                window.location.href = '?page=bid_optimizer';
            }
            // Alt + 2: Campaigns Optimizer
            if (e.altKey && e.key === '2') {
                window.location.href = '?page=campaigns_optimizer';
            }
        });
        </script>
        """,
        height=0
    )
```

## 10. Mobile Navigation (Not Supported)

### Mobile Detection
```python
def check_mobile():
    """Detect mobile device and show message"""
    
    # CSS media query approach
    st.markdown(
        """
        <style>
        @media (max-width: 1024px) {
            .main-content {
                display: none;
            }
            .mobile-warning {
                display: block;
                text-align: center;
                padding: 50px;
                font-size: 18px;
            }
        }
        </style>
        <div class="mobile-warning" style="display: none;">
            Please use a desktop browser to access this application.
        </div>
        """,
        unsafe_allow_html=True
    )
```

## 11. Navigation Analytics (Optional)

### Tracking Page Views
```python
def track_navigation(from_page: str, to_page: str):
    """Track navigation for analytics"""
    
    if 'navigation_history' not in st.session_state:
        st.session_state.navigation_history = []
    
    st.session_state.navigation_history.append({
        'from': from_page,
        'to': to_page,
        'timestamp': datetime.now(),
        'session_id': st.session_state.get('session_id')
    })
```

## 12. Error Handling

### Navigation Errors
```python
def handle_navigation_error(error: Exception):
    """Handle navigation errors gracefully"""
    
    st.error(f"Navigation error: {str(error)}")
    
    # Fallback to default page
    st.session_state.current_page = 'bid_optimizer'
    
    # Log error
    log_error('navigation', error)
    
    # Allow recovery
    if st.button("Return to Home"):
        reset_navigation()
```

## 13. Future Navigation (TBD)

### Phase 5-6 Additions
```python
# TBD - Additional pages
FUTURE_PAGES = {
    'settings': {
        'title': 'SETTINGS',
        'enabled': False
    },
    'help': {
        'title': 'HELP',
        'enabled': False
    }
}
```

### Sub-Navigation
```python
# TBD - Sub-navigation within Campaigns Optimizer
CAMPAIGNS_TABS = {
    'negation': 'Negation',
    'harvesting': 'Harvesting'
}
```